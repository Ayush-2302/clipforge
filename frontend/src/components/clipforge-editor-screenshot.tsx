import Image from "next/image";

/** The sample editor capture predates the ClipForge name; cover its old wordmark. */
export function ClipForgeEditorScreenshot({ alt }: { alt: string }) {
  return (
    <div className="relative overflow-hidden">
      <Image
        src="/blog/clipforge-editor.webp"
        alt={alt}
        width={1800}
        height={1109}
        sizes="(max-width: 768px) 100vw, 768px"
        className="h-auto w-full"
      />
      <span
        aria-hidden="true"
        className="absolute left-[15.8%] top-[0.6%] z-10 flex h-[3.8%] w-[8%] items-center justify-center bg-white px-1 font-sans text-[clamp(6px,0.55vw,10px)] font-bold leading-none text-black"
      >
        ClipForge AI
      </span>
    </div>
  );
}
