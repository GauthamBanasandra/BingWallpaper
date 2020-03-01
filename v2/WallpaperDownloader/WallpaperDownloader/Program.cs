using System;

namespace WallpaperDownloader
{
    class Program
    {
        static void Main(string[] args)
        {
            var outputDir = @"C:\Users\Gautham\Pictures\Wallpapers";
            var client = new SmartClient(outputDir);
            client.Download();
        }
    }
}
