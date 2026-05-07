/*
 Navicat MySQL Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : stone_db

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 19/09/2025 10:51:10

 石材数据库分表设计
*/

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS stone_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- 切换到 stone_db
USE stone_db;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for production_orders
-- ----------------------------
DROP TABLE IF EXISTS `production_orders`;
CREATE TABLE `production_orders` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '内部自增ID',
  `production_order_number` varchar(50) NOT NULL COMMENT '生产单号',
  `order_date` date NOT NULL COMMENT '下单日期',
  `delivery_date` date NOT NULL COMMENT '发货日期',
  `customer` varchar(100) NOT NULL COMMENT '客户',
  `project_name` varchar(200) NOT NULL COMMENT '工程名',
  `material` varchar(100) NOT NULL COMMENT '材料',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建数据行的日期',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改数据行的日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_production_order_number` (`production_order_number`),
  KEY `idx_customer` (`customer`),
  KEY `idx_order_date` (`order_date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='生产订单基础信息表';

-- ----------------------------
-- Records of production_orders
-- ----------------------------
BEGIN;
INSERT INTO `production_orders` VALUES (1, '25-5-181', '2025-05-27', '2025-06-03', '清松', '北京九章别墅公区地面', '威尼斯棕', '2025-09-18 17:35:04', '2025-09-18 17:35:04');
COMMIT;


CREATE TABLE `stone_items` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '内部自增ID',
  `composite_identifier` varchar(150) NOT NULL COMMENT '组合唯一标识（单号+编号前缀+编号）',
  `production_order_number` varchar(50) NOT NULL COMMENT '生产单号',
  `installation_location` varchar(200) NOT NULL COMMENT '安装部位',
  `number_prefix` varchar(20) DEFAULT NULL COMMENT '编号前缀',
  `number` varchar(50) NOT NULL COMMENT '编号',
  `length` int NOT NULL COMMENT '长L(mm)',
  `width` int NOT NULL COMMENT '宽W(mm)',
  `thickness` int NOT NULL COMMENT '厚T(mm)',
  `quantity` int NOT NULL COMMENT '数量(pcs)',
  `square_area` decimal(10,2) GENERATED ALWAYS AS ((((`length` * `width`) * `quantity`) / 1000000)) STORED COMMENT '平方数(m²)【系统会自动计算，保留两位小数】',
  `processing_method_note` varchar(500) DEFAULT NULL COMMENT '加工方式备注',
  `box_number` varchar(50) DEFAULT NULL COMMENT '箱号',
  `drawing_page` varchar(50) DEFAULT NULL COMMENT '图页',
  `scale_url` varchar(500) DEFAULT NULL COMMENT '量尺图片URL',
  `cutting_status` tinyint DEFAULT '0' COMMENT '-1:异常, 0:待切割, 1:切割中, 2:已完成',
  `operator_user_id` int DEFAULT NULL COMMENT '操作人员ID（关联users表）',
  `cutting_start_time` timestamp NULL DEFAULT NULL COMMENT '切割开始时间',
  `cutting_end_time` timestamp NULL DEFAULT NULL COMMENT '切割完成时间',
  `processing_type` CHAR(4) NOT NULL DEFAULT '0000' COMMENT '加工工艺：每位0-5, 上下左右',
  `cutting_meters` DECIMAL(10,3) NOT NULL DEFAULT 0.000 COMMENT '切割米数，根据加工工艺和长宽计算',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建数据行的日期',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改数据行的日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_composite_identifier` (`composite_identifier`),
  KEY `idx_production_order_number` (`production_order_number`),
  KEY `idx_operator_user_id` (`operator_user_id`),
  KEY `idx_cutting_time_range` (`cutting_start_time`,`cutting_end_time`),
  KEY `idx_operator_cutting_status` (`operator_user_id`,`cutting_status`),
  CONSTRAINT `fk_stone_items_operator` FOREIGN KEY (`operator_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_stone_items_order` FOREIGN KEY (`production_order_number`) REFERENCES `production_orders` (`production_order_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='石材明细信息表';

-- 触发器：自动计算 cutting_meters
DELIMITER $$

-- 插入前计算 cutting_meters
CREATE TRIGGER `trg_stone_items_cutting_meters_insert`
BEFORE INSERT ON `stone_items`
FOR EACH ROW
BEGIN
    DECLARE l_count INT DEFAULT 0;
    DECLARE w_count INT DEFAULT 0;

    -- 统计前两位不为0的数量
    IF SUBSTRING(NEW.processing_type,1,1) != '0' THEN
        SET l_count = l_count + 1;
    END IF;
    IF SUBSTRING(NEW.processing_type,2,1) != '0' THEN
        SET l_count = l_count + 1;
    END IF;

    -- 统计后两位不为0的数量
    IF SUBSTRING(NEW.processing_type,3,1) != '0' THEN
        SET w_count = w_count + 1;
    END IF;
    IF SUBSTRING(NEW.processing_type,4,1) != '0' THEN
        SET w_count = w_count + 1;
    END IF;

    -- 计算切割米数
    SET NEW.cutting_meters = (l_count * NEW.length + w_count * NEW.width) / 1000;
END$$

-- 更新前计算 cutting_meters
CREATE TRIGGER `trg_stone_items_cutting_meters_update`
BEFORE UPDATE ON `stone_items`
FOR EACH ROW
BEGIN
    DECLARE l_count INT DEFAULT 0;
    DECLARE w_count INT DEFAULT 0;

    IF SUBSTRING(NEW.processing_type,1,1) != '0' THEN
        SET l_count = l_count + 1;
    END IF;
    IF SUBSTRING(NEW.processing_type,2,1) != '0' THEN
        SET l_count = l_count + 1;
    END IF;

    IF SUBSTRING(NEW.processing_type,3,1) != '0' THEN
        SET w_count = w_count + 1;
    END IF;
    IF SUBSTRING(NEW.processing_type,4,1) != '0' THEN
        SET w_count = w_count + 1;
    END IF;

    SET NEW.cutting_meters = (l_count * NEW.length + w_count * NEW.width) / 1000;
END$$

DELIMITER ;

-- ----------------------------
-- Records of stone_items
-- ----------------------------
BEGIN;
INSERT INTO stone_items (
    composite_identifier,
    production_order_number,
    installation_location,
    number_prefix,
    number,
    length,
    width,
    thickness,
    quantity,
    processing_method_note,
    box_number,
    drawing_page,
    scale_url,
    cutting_status,
    operator_user_id,
    cutting_start_time,
    cutting_end_time,
    processing_type,
    created_at,
    updated_at
) VALUES
('25-5-181A102','25-5-181','负一层公区地面',NULL,'A102',810,400,18,1,'下长正倒3*3直边见光','4#','3',NULL,0,3,NULL,NULL,'0100','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A2','25-5-181','负一层公区地面',NULL,'A2',1530,352,18,1,NULL,'1#','2',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A98','25-5-181','负一层公区地面',NULL,'A98',1530,595,18,1,NULL,'3#','2',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A5','25-5-181','负一层公区地面',NULL,'A5',672,352,18,1,NULL,'1#','2',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A6','25-5-181','负一层公区地面',NULL,'A6',1102,930,18,1,NULL,'1#','2',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A177','25-5-181','负一层公区地面',NULL,'A177',300,800,18,1,'右宽正倒3*3直边见光','6#','3',NULL,1,3,'2025-09-18 14:07:20','2025-09-18 15:07:15','0100','2025-09-18 13:26:02','2025-09-19 10:49:31'),
('25-5-181A178','25-5-181','负一层公区地面',NULL,'A178',1145,930,18,1,NULL,'6#','3',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A179','25-5-181','负一层公区地面',NULL,'A179',1145,930,18,1,NULL,'6#','3',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02'),
('25-5-181A180','25-5-181','负一层公区地面',NULL,'A180',1145,930,18,1,NULL,'6#','3',NULL,0,3,NULL,NULL,'0000','2025-09-18 13:26:02','2025-09-18 13:26:02');
COMMIT;


-- ----------------------------
-- Table structure for stone_measurements
-- ----------------------------
DROP TABLE IF EXISTS `stone_measurements`;
CREATE TABLE `stone_measurements` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '内部自增ID',
  `composite_identifier` varchar(150) NOT NULL COMMENT '关联石材明细（composite_identifier）',
  `scan_length` decimal(10,3) NOT NULL COMMENT '扫描长度(mm)',
  `scan_width` decimal(10,3) NOT NULL COMMENT '扫描宽度(mm)',
  `original_url` varchar(500) DEFAULT NULL COMMENT '原始图片URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建/扫描时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_measurement_composite` (`composite_identifier`),
  CONSTRAINT `fk_measurement_stone_item` FOREIGN KEY (`composite_identifier`) REFERENCES `stone_items` (`composite_identifier`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='石材尺寸检测数据表';

-- ----------------------------
-- Records of stone_measurements
-- ----------------------------
BEGIN;
INSERT INTO `stone_measurements` VALUES (1, '25-5-181A102', 810.000, 400.000, NULL, '2025-09-18 13:26:02', '2025-09-18 13:26:02');
INSERT INTO `stone_measurements` VALUES (2, '25-5-181A177', 300.000, 800.000, NULL, '2025-09-17 13:26:02', '2025-09-17 14:53:59');
COMMIT;

-- ----------------------------
-- Table structure for stone_processing_status
-- ----------------------------
DROP TABLE IF EXISTS `stone_processing_status`;
CREATE TABLE `stone_processing_status` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '内部自增ID',
  `composite_identifier` varchar(150) NOT NULL COMMENT '组合唯一标识（关联石材明细）',
  `missing_corners` int DEFAULT NULL COMMENT '缺角数',
  `stains` int DEFAULT NULL COMMENT '污渍数',
  `cracks` int DEFAULT NULL COMMENT '裂纹数',
  `total_defects` int GENERATED ALWAYS AS (((coalesce(`missing_corners`,0) + coalesce(`stains`,0)) + coalesce(`cracks`,0))) STORED COMMENT '缺陷总数',
  `defect_url` varchar(500) DEFAULT NULL COMMENT '缺陷图片URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建/缺陷检测日期',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新数据行的日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_composite_identifier` (`composite_identifier`),
  KEY `idx_total_defects` (`total_defects`),
  CONSTRAINT `fk_stone_status_item` FOREIGN KEY (`composite_identifier`) REFERENCES `stone_items` (`composite_identifier`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='石材加工状态表';

-- ----------------------------
-- Records of stone_processing_status
-- ----------------------------
BEGIN;
INSERT INTO `stone_processing_status` VALUES (1, '25-5-181A180', 1, 2, NULL, DEFAULT, NULL, '2025-09-18 22:08:39', '2025-09-18 22:08:39');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) NOT NULL COMMENT '登录用户名（唯一）',
  `fullname` varchar(50) NOT NULL COMMENT '中文用户名（唯一）',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `role` enum('superadmin','admin','productor','undefined','production') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'undefined' COMMENT '权限角色',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `lastLogin_at` timestamp NULL DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统用户表';

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1, 'superAdmin', '超级管理员', '123456', 'superadmin', '2025-09-18 13:26:02', '2025-09-18 13:26:02', '2025-09-18 13:26:02');
INSERT INTO `users` VALUES (2, 'admin', '管理员', '123456', 'admin', '2025-09-18 13:26:02', '2025-09-18 23:11:20', '2025-09-18 23:11:20');
INSERT INTO `users` VALUES (3, 'user', '生产用户','123456', 'productor', '2025-09-18 13:26:02', '2025-09-18 22:45:25', '2025-09-18 13:26:02');
INSERT INTO `users` VALUES (4, '1111', '测试1','11', 'undefined', '2025-09-18 16:12:47', '2025-09-18 16:12:47', '2025-09-18 13:26:02');
INSERT INTO `users` VALUES (5, '1', '测试2', '1', 'productor', '2025-09-18 13:26:02', '2025-09-19 10:35:44', '2025-09-19 10:35:45');
INSERT INTO `users` VALUES (6, '2', '测试3', '1', 'undefined', '2025-09-18 21:01:44', '2025-09-18 23:11:42', NULL);
INSERT INTO `users` VALUES (7, 'ceshi2', '测试4','ceshi', 'admin', '2025-09-18 21:01:44', '2025-09-18 21:33:44', NULL);
COMMIT;

-- ----------------------------
-- View structure for v_complete_stone_info
-- ----------------------------
-- 删除旧视图（如果存在）
DROP VIEW IF EXISTS `v_complete_stone_info`;

-- 创建新视图（不再引用 stone_item_details）
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `v_complete_stone_info` AS
SELECT
    si.id AS stone_item_id,
    si.composite_identifier,
    po.production_order_number,
    po.order_date,
    po.delivery_date,
    po.customer,
    po.project_name,
    po.material,
    si.installation_location,
    si.number_prefix,
    si.number,
    si.length,
    si.width,
    si.thickness,
    si.quantity,
    si.square_area,
    si.processing_method_note,
    si.box_number,
    si.drawing_page,
    si.scale_url,
    si.cutting_status,
    si.operator_user_id,
    u.username AS operator_username,
    si.cutting_start_time,
    si.cutting_end_time,
    sps.missing_corners,
    sps.stains,
    sps.cracks,
    sps.total_defects,
    sps.defect_url,
    si.cutting_meters,
    sm.scan_length,
    sm.scan_width,
    sm.original_url AS measurement_url,
    si.created_at,
    si.updated_at
FROM stone_items si
LEFT JOIN production_orders po
    ON si.production_order_number = po.production_order_number
LEFT JOIN stone_processing_status sps
    ON si.composite_identifier = sps.composite_identifier
LEFT JOIN users u
    ON si.operator_user_id = u.id
LEFT JOIN stone_measurements sm
    ON si.composite_identifier = sm.composite_identifier;

SET FOREIGN_KEY_CHECKS = 1;
