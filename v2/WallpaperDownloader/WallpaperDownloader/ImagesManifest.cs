using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace WallpaperDownloader
{
    class ImagesManifest
    {
        private readonly string outputDir;
        private readonly string manifestPath;
        private HashSet<string> imagesHashes;

        public ImagesManifest(string outputDir)
        {
            this.outputDir = outputDir;
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

        private string GetHash(byte[] data)
        {
            using MD5 md5 = MD5.Create();
            var hash = md5.ComputeHash(data);

            StringBuilder builder = new StringBuilder();
            for (int i = 0; i < hash.Length; i++)
            {
                builder.Append(hash[i].ToString("X2"));
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
