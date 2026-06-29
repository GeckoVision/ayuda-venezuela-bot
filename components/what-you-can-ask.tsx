interface Props {
  t: Record<string, string>;
}

const CARD_KEYS = ["ask_1", "ask_2", "ask_3", "ask_4"] as const;

export default function WhatYouCanAsk({ t }: Props) {
  return (
    <section className="py-14 md:py-16">
      <div className="mx-auto max-w-[920px] px-5">
        <h2 className="text-[clamp(22px,4vw,30px)] font-extrabold text-center tracking-tight mb-2 text-balance">
          {t.ask_title}
        </h2>
        <p className="text-center text-muted max-w-[560px] mx-auto mb-9 text-pretty">
          {t.ask_lead}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          {CARD_KEYS.map((key) => (
            <div
              key={key}
              className="bg-card border border-line rounded-[16px] px-5 py-5 flex gap-3 items-start"
            >
              <span className="text-blue font-extrabold text-[18px] leading-none mt-0.5 select-none">
                &ldquo;
              </span>
              <p className="text-[17px] font-semibold text-ink leading-snug">
                {t[key]}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
