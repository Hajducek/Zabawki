import win32gui
import win32ui
import win32con
import win32api

hdesktop = win32gui.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
heigth = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

desktop_dc = win32gui.GetWindowDC(desktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

mem_dc = img_dc.CreateCompatibileDC()

screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibileBitmap(img_dc, width, heigth)
mem_dc.SelectObject(screenshot)
mem_dc.BitBlt((0, 0), (width, heigth), img_dc, (left, top), win32con.SRCCOPY)

screenshot.SaveBitmapFile(mem_dc, 'c:\\windows\\Temp\\screenshot.bmp')

mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
