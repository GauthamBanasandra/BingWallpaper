using Newtonsoft.Json;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace WallpaperDownloader
{
    class ImagesManifest
    {
        private readonly string manifestPath;
        private readonly HashSet<string> imagesHashes;

        public ImagesManifest(string outputDir)
        {
            manifestPath = $"{outputDir}/manifest.json";
            imagesHashes = new HashSet<string>();
            ReadOrCreateManifest();
        }

        private void ReadOrCreateManifest()
        {
            var fileStream = new FileStream(manifestPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None);
            StreamReader streamReader = new StreamReader(fileStream);

            var content = streamReader.ReadToEnd();
            streamReader.Close();

            foreach (var hash in JsonConvert.DeserializeObject<List<string>>(content) ?? Enumerable.Empty<string>())
            {
                imagesHashes.Add(hash);
            }
        }

        private static string GetHash(byte[] data)
        {
            using var hasher = SHA512.Create();
            var hash = hasher.ComputeHash(data);

            StringBuilder builder = new StringBuilder();
            for (int i = 0; i < hash.Length; i++)
            {
                builder.Append(hash[i].ToString("X2", CultureInfo.InvariantCulture));
            }
            return builder.ToString();
        }

        public bool IsPresent(byte[] image)
        {
            var hash = GetHash(image);
            return imagesHashes.Contains(hash);
        }

        public void AddImage(byte[] image)
        {
            var hash = GetHash(image);
            imagesHashes.Add(hash);

            var json = JsonConvert.SerializeObject(imagesHashes);
            File.WriteAllText(manifestPath, json);
        }
    }
}
