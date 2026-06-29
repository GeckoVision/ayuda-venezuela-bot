import { TelegramIcon } from "./icons";

interface HeroProps {
  t: Record<string, string>;
}

export default function Hero({ t }: HeroProps) {
  return (
    <section
      className="text-white text-center py-16 md:py-20"
      style={{
        background:
          "radial-gradient(1200px 500px at 70% -10%, #12325c, #0b1f3a)",
      }}
    >
      <div className="mx-auto max-w-[920px] px-5">
        {/* Eyebrow */}
        <span className="inline-block text-[13px] font-bold tracking-[1.5px] uppercase text-yellow bg-yellow/12 px-3 py-1.5 rounded-full mb-5">
          {t.eyebrow}
        </span>

        {/* Heading */}
        <h1 className="text-[clamp(30px,6vw,46px)] leading-[1.12] font-extrabold tracking-tight mb-4 text-balance">
          {t.hero_h1}
        </h1>

        {/* Sub */}
        <p className="text-[clamp(16px,2.4vw,20px)] text-subtle max-w-[620px] mx-auto mb-8 leading-relaxed text-pretty">
          {t.hero_sub}
        </p>

        {/* CTAs */}
        <div className="flex gap-3 justify-center flex-wrap items-center">
          <a
            href="https://t.me/DEV_VEZbot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2.5 font-bold px-6 py-3.5 rounded-full text-[17px] text-white transition-transform hover:-translate-y-px focus-visible:outline-2 focus-visible:outline-white"
            style={{
              background: "#229ed9",
              boxShadow: "0 8px 24px rgba(34,158,217,0.4)",
            }}
          >
            <TelegramIcon className="w-[22px] h-[22px]" aria-hidden="true" />
            {t.cta_open}
          </a>
          <a
            href="https://t.me/DEV_VEZbot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2.5 font-bold px-6 py-3.5 rounded-full text-[17px] text-white border border-white/22 bg-white/8 transition-transform hover:-translate-y-px focus-visible:outline-2 focus-visible:outline-white"
          >
            @DEV_VEZbot
          </a>
        </div>

        <p className="mt-5 text-[14px] text-subtle">{t.trust}</p>
      </div>
    </section>
  );
}
