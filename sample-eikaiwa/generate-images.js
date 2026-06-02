const fs = require("node:fs/promises");
const path = require("node:path");
const { spawn } = require("node:child_process");

const apiKey = process.env.OPENAI_API_KEY;
const outputDir = path.join(__dirname, "images");

const images = [
  {
    fileName: "hero.jpg",
    width: 1280,
    height: 720,
    prompt:
      "A bright, modern English language school classroom with large windows, natural lighting. Japanese adult students engaged in lively conversation with a foreign teacher. Warm, welcoming atmosphere. High quality, photorealistic.",
  },
  {
    fileName: "instructor-01.jpg",
    width: 400,
    height: 400,
    prompt:
      "Professional headshot portrait of an American male English teacher in his 30s, friendly smile, business casual attire, white background, high quality photorealistic",
  },
  {
    fileName: "instructor-02.jpg",
    width: 400,
    height: 400,
    prompt:
      "Professional headshot portrait of a British female English teacher in her 30s, warm smile, professional attire, white background, high quality photorealistic",
  },
  {
    fileName: "instructor-03.jpg",
    width: 400,
    height: 400,
    prompt:
      "Professional headshot portrait of a Canadian male English teacher in his 30s, confident smile, smart casual attire, white background, high quality photorealistic",
  },
  {
    fileName: "feature-business.jpg",
    width: 800,
    height: 500,
    prompt:
      "Japanese businessperson confidently presenting in English at a modern office meeting room, diverse international colleagues listening. Professional atmosphere. High quality photorealistic.",
  },
  {
    fileName: "feature-lesson.jpg",
    width: 800,
    height: 500,
    prompt:
      "Japanese adult student doing an online English video call lesson on a laptop at home, smiling, notebook open, cozy study environment. High quality photorealistic.",
  },
  {
    fileName: "feature-flexible.jpg",
    width: 800,
    height: 500,
    prompt:
      "Person studying English on a smartphone during commute on a Tokyo train, natural lighting, modern urban setting. High quality photorealistic.",
  },
];

function openAiSize(width, height) {
  const ratio = width / height;
  if (ratio > 1.2) return "1792x1024";
  if (ratio < 0.8) return "1024x1792";
  return "1024x1024";
}

function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
      } else {
        reject(new Error(`${command} exited with ${code}: ${stderr || stdout}`));
      }
    });
  });
}

async function maybeLoadSharp() {
  try {
    return require("sharp");
  } catch {
    return null;
  }
}

async function callImageApi(payload) {
  const response = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const text = await response.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    body = { raw: text };
  }

  if (!response.ok) {
    const message = body?.error?.message || text || `HTTP ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.body = body;
    throw error;
  }

  return body;
}

async function generateImage({ prompt, width, height }) {
  const size = openAiSize(width, height);
  const basePayload = {
    model: "dall-e-3",
    prompt,
    n: 1,
    size,
    quality: "standard",
    response_format: "b64_json",
  };

  try {
    const body = await callImageApi(basePayload);
    return {
      buffer: Buffer.from(body.data[0].b64_json, "base64"),
      sourceSize: size,
    };
  } catch (error) {
    const message = String(error.message || "");
    const canRetryWithUrl =
      error.status === 400 &&
      (message.includes("response_format") || message.includes("b64_json"));

    if (!canRetryWithUrl) throw error;

    const fallbackPayload = { ...basePayload };
    delete fallbackPayload.response_format;
    const body = await callImageApi(fallbackPayload);
    const imageResponse = await fetch(body.data[0].url);
    if (!imageResponse.ok) {
      throw new Error(`Failed to download generated image: HTTP ${imageResponse.status}`);
    }
    return {
      buffer: Buffer.from(await imageResponse.arrayBuffer()),
      sourceSize: size,
    };
  }
}

async function saveAsJpeg(inputBuffer, outputPath, width, height, sharp) {
  if (sharp) {
    await sharp(inputBuffer)
      .resize(width, height, { fit: "cover", position: "centre" })
      .jpeg({ quality: 90 })
      .toFile(outputPath);
    return "sharp";
  }

  const tmpPath = `${outputPath}.tmp`;
  await fs.writeFile(tmpPath, inputBuffer);

  try {
    await run("sips", ["-s", "format", "jpeg", "-z", String(height), String(width), tmpPath, "--out", outputPath]);
    await fs.rm(tmpPath, { force: true });
    return "sips";
  } catch (error) {
    await fs.rename(tmpPath, outputPath);
    console.warn(`Resize/convert fallback failed for ${path.basename(outputPath)}: ${error.message}`);
    return "raw";
  }
}

async function main() {
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY is not set.");
  }

  await fs.mkdir(outputDir, { recursive: true });
  const sharp = await maybeLoadSharp();

  console.log(`Image processor: ${sharp ? "sharp" : "sips fallback"}`);

  for (const image of images) {
    console.log(`Generating ${image.fileName} (${image.width}x${image.height})...`);
    const generated = await generateImage(image);
    const outputPath = path.join(outputDir, image.fileName);
    const processor = await saveAsJpeg(generated.buffer, outputPath, image.width, image.height, sharp);
    console.log(
      `Completed ${image.fileName}: generated ${generated.sourceSize}, saved ${image.width}x${image.height} JPEG via ${processor}`
    );
  }

  console.log("All images generated.");
}

main().catch((error) => {
  console.error("Image generation failed.");
  console.error(error?.body ? JSON.stringify(error.body, null, 2) : error.message);
  process.exitCode = 1;
});
