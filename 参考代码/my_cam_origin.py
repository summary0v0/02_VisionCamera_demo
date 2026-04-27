# _*_ coding: utf-8 -*_
import stone_vision_detector.infrastructure.camera.IKapBoard as IKapBoard
import ctypes
import os
import tkinter
from tkinter import filedialog
import time

# Define frame count
DEFINE_FRAME_COUNT = 1


class IKapBoardGrabLineTrigger:
    def __init__(self, save_path):
        # Device handle
        self.m_hDev = ctypes.c_void_p(None)
        # Grab frame index
        self.m_nCurFrameIndex = ctypes.c_uint(0)
        # Buffer data
        self.m_bufferData = ctypes.c_void_p(None)

        # Callback
        self.grabStartProc = ctypes.c_void_p(None)
        self.grabStopProc = ctypes.c_void_p(None)
        self.frameReadyProc = ctypes.c_void_p(None)
        self.timeoutProc = ctypes.c_void_p(None)
        self.frameLostProc = ctypes.c_void_p(None)
        self.save_path = save_path

    # Get Board count
    @staticmethod
    def GetBoardCount():
        res, nBoardCount = IKapBoard.IKapGetBoardCount(IKapBoard.IKBoardPCIE)
        for nIndex in range(0, nBoardCount, 1):
            res, strBoardName = IKapBoard.IKapGetBoardName(IKapBoard.IKBoardPCIE, nIndex)
            if res == IKapBoard.IK_RTN_OK:
                print(strBoardName)
        return nBoardCount

    # Open device
    def OpenDevice(self, nIndex):
        self.m_hDev = IKapBoard.IKapOpen(IKapBoard.IKBoardPCIE, nIndex)
        if self.m_hDev == None or self.m_hDev == -1:
            return False
        return True

    # Whether the device is on
    def IsOpenDevice(self):
        if self.m_hDev == None or self.m_hDev == -1:
            return False
        return True

    # Close device
    def CloseDevice(self):
        if not self.IsOpenDevice():
            return
        IKapBoard.IKapClose(self.m_hDev)

    # Load configuration test
    def LoadConfigurationFile(self, strFileName):
        res = IKapBoard.IKapLoadConfigurationFromFile(self.m_hDev, strFileName)
        if res == IKapBoard.IK_RTN_OK:
            return True
        return False

    # Set line triggger
    def SetLineTrigger(self):
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_CC1_SOURCE,
                                    IKapBoard.IKP_CC_SOURCE_VAL_INTEGRATION_SIGNAL1)
        if res != IKapBoard.IK_RTN_OK:
            return False
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE,
                                    IKapBoard.IKP_INTEGRATION_TRIGGER_SOURCE_VAL_SHAFT_ENCODER1)
        if res != IKapBoard.IK_RTN_OK:
            return False
        return True

    # Start grab
    def StartGrab(self, nFrameCount):
        # Set frame count
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT, DEFINE_FRAME_COUNT)
        if res != IKapBoard.IK_RTN_OK:
            return False
        # Set timeout
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_TIME_OUT, -1)
        if res != IKapBoard.IK_RTN_OK:
            return False
        # Set grab mode
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_GRAB_MODE, IKapBoard.IKP_GRAB_NON_BLOCK)
        if res != IKapBoard.IK_RTN_OK:
            return False
        # Set transfer mode
        res = IKapBoard.IKapSetInfo(self.m_hDev, IKapBoard.IKP_FRAME_TRANSFER_MODE,
                                    IKapBoard.IKP_FRAME_TRANSFER_SYNCHRONOUS_NEXT_EMPTY_WITH_PROTECT)
        if res != IKapBoard.IK_RTN_OK:
            return False

        # Apply buffer data
        res, bufferSize = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_SIZE)
        if res != IKapBoard.IK_RTN_OK:
            return False
        self.m_bufferData = ctypes.create_string_buffer(bufferSize)
        if self.m_bufferData == None:
            print("Apply buffer data failure")
            return False

        # Get image param
        res, nWidth = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_WIDTH)
        res, nHeight = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_HEIGHT)
        res, nDataFormat = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_DATA_FORMAT)
        res, nImageType = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_IMAGE_TYPE)
        if nDataFormat == 8:
            nDepth = 8
        else:
            nDepth = 16

        if nImageType == IKapBoard.IKP_IMAGE_TYPE_VAL_MONOCHROME:
            nChannel = 1
        elif nImageType == IKapBoard.IKP_IMAGE_TYPE_VAL_RGB or nImageType == IKapBoard.IKP_IMAGE_TYPE_VAL_BGR:
            nChannel = 3
        else:
            nChannel = 4
        print("Width = %d,Height = %d,Detph = %d,Channel = %d" % (nWidth, nHeight, nDepth, nChannel))

        # # Register callback
        self.grabStartProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onGrabStartProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStart, self.grabStartProc,
                                       ctypes.c_void_p(None))
        self.grabStopProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onGrabStopProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStop, self.grabStopProc,
                                       ctypes.c_void_p(None))
        self.frameReadyProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onFrameReadyProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady, self.frameReadyProc,
                                       ctypes.c_void_p(None))
        self.timeoutProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onTimeoutProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_TimeOut, self.timeoutProc, ctypes.c_void_p(None))
        self.frameLostProc = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self.onFrameLostProc)
        IKapBoard.IKapRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameLost, self.frameLostProc,
                                       ctypes.c_void_p(None))
        # Start grab
        res = IKapBoard.IKapStartGrab(self.m_hDev, 0)
        if res != IKapBoard.IK_RTN_OK:
            return False
        return True

    # Stop grab
    def StopGrab(self):
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStart)
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_GrabStop)
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameReady)
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_TimeOut)
        IKapBoard.IKapUnRegisterCallback(self.m_hDev, IKapBoard.IKEvent_FrameLost)
        IKapBoard.IKapStopGrab(self.m_hDev)
        return True

    def onGrabStartProc(self, pParam):
        print("Start grab")

    def onGrabStopProc(self, pParam):
        print("Stop grab")

    def onFrameReadyProc(self, pParam):
        print("Frame ready")
        pUserBuffer = ctypes.c_void_p(None)
        res, bufferStatus = IKapBoard.IKapGetBufferStatus(self.m_hDev, self.m_nCurFrameIndex)
        res, nFrameCount = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_COUNT)

        if bufferStatus.uFull == 1:
            res, nFrameSize = IKapBoard.IKapGetInfo(self.m_hDev, IKapBoard.IKP_FRAME_SIZE)
            IKapBoard.IKapGetBufferAddress(self.m_hDev, self.m_nCurFrameIndex, pUserBuffer)

            # Copy data
            self.m_bufferData = (nFrameSize * ctypes.c_ubyte).from_address(pUserBuffer.value)
            """ Save image data
            fp = open('D:\\IKapBoard.raw','wb')
            fp.write(self.m_bufferData)
            fp.close()
            """
            fp = open(f"{self.save_path}/{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.raw", 'wb')
            fp.write(self.m_bufferData)
            fp.close()

        self.m_nCurFrameIndex.value = (self.m_nCurFrameIndex.value + 1) % DEFINE_FRAME_COUNT

    def onTimeoutProc(self, pParam):
        print("Grab timeout")

    def onFrameLostProc(self, pParam):
        print("Grab frame lost")


def main():
    IKapBoardGrabLineTrigger.GetBoardCount()
    grab = IKapBoardGrabLineTrigger()
    # Open device
    if not grab.OpenDevice(0):
        print("Open device failure")
        os._exit(0)

    # Load configuration test
    root = tkinter.Tk()
    root.withdraw()
    fileName = filedialog.askopenfilename(title=b'Selected File', filetypes=[('vlcf', '*.vlcf')],
                                          initialdir=(os.path.expanduser(b'File Path')))
    if len(fileName) == 0:
        print("Fail to get configuration, using default setting")
    else:
        print(fileName)
        if not grab.LoadConfigurationFile(fileName.encode('utf-8')):
            print("Load configuration test failure")
            os._exit(0)

    # Set line trigger
    if not grab.SetLineTrigger():
        print("Set line trigger failure")
        os._exit(0)

    # Start grab
    if not grab.StartGrab(0):
        print("Start grab failure")
        os._exit(0)

    # Wait
    input()

    # Stop Grab
    grab.StopGrab()

    # Close


