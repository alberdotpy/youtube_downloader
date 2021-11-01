from pytube import YouTube
from time import time
from db import update_db, query_table
from errorhandling import error_handling
import os
import wx
import wx.grid


class Robot(wx.Frame):
    def __init__(self, parent, title):
        super(Robot, self).__init__(parent, title=title, size=(700, 280))
        self.init_ui()
        self.Centre()
        self.SetTitle("Youtube Downloader")
        try:
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap("img\\logo.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
        except Exception as e:
            print("The favicon was not found, please save the favicon in the img directory as icon.png")

    def init_ui(self):
        nb = wx.Notebook(self)
        nb.AddPage(Panel1(nb), "App")
        nb.AddPage(Panel2(nb), "Data")
        self.Show(True)


class Panel1(wx.Panel):
    def __init__(self, parent):
        super(Panel1, self).__init__(parent)
        sizer = wx.GridBagSizer(5, 5)

        # Header
        try:
            imageFile = "img\\logo.png"
            png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            png = scale_bitmap(png, 90, 60)
            logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
            sizer.Add(logo, pos=(0, 0), span=(1, 6), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=10)
        except Exception as e:
            print("The logo file was not found, please save the logo file in the img directory as logo.png")

        lbl_instructions = wx.StaticText(self, label='Video URL : ')
        sizer.Add(lbl_instructions, pos=(1, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.input_url = wx.TextCtrl(self, value="")
        sizer.Add(self.input_url, pos=(1, 1), span=(1, 3), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        lbl_res = wx.StaticText(self, label='Resolution : ')
        sizer.Add(lbl_res, pos=(2, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        resolutions = ['best', '720p', '480p', '360p', '240p', '144p']
        self.resolution = wx.ComboBox(self, choices=resolutions, value='480p')
        sizer.Add(self.resolution, pos=(2, 1), flag=wx.LEFT, border=15)

        btn_download = wx.Button(self, label="Download")
        sizer.Add(btn_download, pos=(3, 0), span=(1, 6), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, border=15)
        self.Bind(wx.EVT_BUTTON, self.onDownload, btn_download)

        # Footer
        line = wx.StaticLine(self)
        sizer.Add(line, pos=(4, 0), span=(1, 6), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        titre = wx.StaticText(self, label="© 2021 - alberdotpy")
        font = wx.Font(7, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        titre.SetFont(font)
        sizer.Add(titre, pos=(5, 0), span=(1, 6), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=5)

        # Sizer
        sizer.AddGrowableCol(3, 0)
        sizer.AddGrowableRow(5, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def onDownload(self, event):
        stime = time()
        err = False
        res = self.resolution.GetValue()
        cwd = os.getcwd()
        yt = self.input_url.GetValue()
        ytvideo = YouTube(yt)

        try:
            print(f"Downloading: {ytvideo.title}")
            if res == 'best':
                ytvideo.streams.filter(progressive=True, file_extension='mp4')\
                    .order_by('resolution').desc().first().download(output_path="videos")
            else:
                ytvideo.streams.get_by_resolution(res).download(output_path="videos")

        except Exception as e:
            err = True
            print(f"An error ocurred while downloading video {ytvideo.title}")
            error_handling(e)

        if not err:
            total_time = time() - stime
            update_db(author=ytvideo.author, title=ytvideo.title, elapsed=total_time)
            print(f"The YouTube Video has been downloaded succesfully in {cwd}\\videos\\")


class Panel2(wx.grid.Grid):
    def __init__(self, parent):
        super(Panel2, self).__init__(parent)
        dt = query_table()
        self.CreateGrid(len(dt), 4)
        grid = wx.grid.Grid(self, -1)
        grid.AutoSizeColumns()
        self.SetColLabelValue(0, "Author")
        self.SetColLabelValue(1, "Video")
        self.SetColLabelValue(2, "Date")
        self.SetColLabelValue(3, "Elapsed")
        for x in range(0, len(dt)):
            self.SetCellValue(x, 0, dt[x][0])
            self.SetCellValue(x, 1, dt[x][1])
            self.SetCellValue(x, 2, str(dt[x][2]).split(":")[0])
            self.SetCellValue(x, 3, str(dt[x][3]).split('.')[0])


def main():
    app = wx.App()
    Robot(None, 'Robot').Show()
    app.MainLoop()


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


if __name__ == '__main__':
    main()






