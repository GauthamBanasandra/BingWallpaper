using System;

namespace WallpaperDownloader
{
    class Program
    {
        static void Main(string[] args)
        {
            var downloader = new Downloader();
            downloader.Download();
        }
    }
}
