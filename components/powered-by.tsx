import { ExternalLink } from "lucide-react";

interface Props {
  t: Record<string, string>;
}

export default function PoweredBy({ t }: Props) {
  return (
    <section className="py-14 md:py-16">
      <div className="mx-auto max-w-[920px] px-5">
        <div className="bg-navy rounded-[22px] px-8 py-10 md:px-12 text-center">
          <h2 className="text-[clamp(22px,4vw,28px)] font-extrabold text-white tracking-tight mb-4 text-balance">
            {t.surf_title}
          </h2>
          <p className="text-subtle max-w-[640px] mx-auto mb-3 leading-relaxed text-pretty">
            {t.surf_p1}
          </p>
          <p className="text-subtle max-w-[640px] mx-auto mb-5 leading-relaxed text-pretty">
            {t.surf_p2}
          </p>

          {/* Privacy note */}
          <div className="border border-white/14 rounded-xl px-4 py-3 max-w-[600px] mx-auto mb-6 bg-white/4 text-[14px] text-subtle">
            {t.surf_note}
          </div>

          <a
            href="https://github.com/GeckoVision/gecko-surf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-yellow font-bold hover:underline text-[15px]"
          >
            {t.surf_cta}
            <ExternalLink size={14} aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>
  );
}
