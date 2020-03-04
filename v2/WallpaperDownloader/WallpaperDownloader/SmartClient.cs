using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;

namespace WallpaperDownloader
{
    class SmartClient
    {
        private Uri baseUrl;
        private readonly string outputDir;
        private readonly Regex rx;
        private ImagesManifest manifest;

        public SmartClient(string outputDir)
        {
            baseUrl = new Uri("https://www.bing.com");
            this.outputDir = outputDir;
            rx = new Regex("href=\"(?<image_href>/hpwp/\\S+)\"", RegexOptions.Compiled);
            manifest = new ImagesManifest(outputDir);
        }

        private async Task<string> LoadPage()
        {
            using var client = new HttpClient();
            var page = await client.GetAsync(baseUrl).ConfigureAwait(true);
            var content = page.Content;
            return await content.ReadAsStringAsync().ConfigureAwait(true);
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
            using var webClient = new WebClient();
            var uri = new Uri(imageUrl);
            var data = webClient.DownloadData(uri);

            if (manifest.IsPresent(data))
            {
                Console.WriteLine(Properties.Resources.SkipSavingImage);
                return;
            }
            manifest.AddImage(data);

            using var stream = new MemoryStream(data);
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
