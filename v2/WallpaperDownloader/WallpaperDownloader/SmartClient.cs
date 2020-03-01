using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;

namespace WallpaperDownloader
{
    class SmartClient
    {
        private const string baseUrl = "https://www.bing.com";
        private readonly string outputDir;
        private readonly Regex rx;
        private ImagesManifest manifest;

        public SmartClient(string outputDir)
        {
            this.outputDir = outputDir;
            rx = new Regex("href=\"(?<image_href>/hpwp/\\S+)\"", RegexOptions.Compiled);
            manifest = new ImagesManifest(outputDir);
        }

        private async Task<string> LoadPage()
        {
            var client = new HttpClient();
            var page = await client.GetAsync(baseUrl);
            var content = page.Content;
            return await content.ReadAsStringAsync();
        }

        private string ExtractImageHref(string content)
        {
            var match = rx.Match(content);
            if (!match.Success)
            {
                return null;
            }
            return match.Groups["image_href"].Value;
        }

        private void DownloadImageAndWriteToFile(string imageUrl)
        {
            var webClient = new WebClient();
            var uri = new Uri(imageUrl);
            var data = webClient.DownloadData(uri);

            if (manifest.IsPresent(data))
            {
                Console.WriteLine("Skipping saving image as it already exists");
                return;
            }
            manifest.AddImage(data);

            var stream = new MemoryStream(data);
            var image = Image.FromStream(stream);

            var outputPath = $@"{outputDir}/{ Guid.NewGuid().ToString()}.jpg";
            image.Save(outputPath, ImageFormat.Jpeg);
        }

        public void Download()
        {
            var content = LoadPage();
            var imageHref = ExtractImageHref(content.Result);
            if (imageHref == null)
            {
                Console.Error.WriteLine("Unable to extract image href");
                return;
            }
            var imageUrl = baseUrl + imageHref;
            DownloadImageAndWriteToFile(imageUrl);
        }
    }
}
