using System;

namespace WallpaperDownloader
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.Error.WriteLine("Please specify the path to store the images");
                return;
            }

            var outputDir = args[0];
            if (!System.IO.Directory.Exists(outputDir))
            {
                Console.Error.WriteLine("The path specified does not exist");
                return;
            }

            var client = new SmartClient(outputDir);
            client.Download();
        }
    }
}
