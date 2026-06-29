interface Props {
  t: Record<string, string>;
}

const STEPS = [
  { n: "1", hKey: "how_1_h", pKey: "how_1_p" },
  { n: "2", hKey: "how_2_h", pKey: "how_2_p" },
  { n: "3", hKey: "how_3_h", pKey: "how_3_p" },
] as const;

export default function HowItWorks({ t }: Props) {
  return (
    <section className="py-14 md:py-16 bg-surface">
      <div className="mx-auto max-w-[920px] px-5">
        <h2 className="text-[clamp(22px,4vw,30px)] font-extrabold text-center tracking-tight mb-2 text-balance">
          {t.how_title}
        </h2>
        <p className="text-center text-muted max-w-[560px] mx-auto mb-10 text-pretty">
          {t.how_lead}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          {STEPS.map(({ n, hKey, pKey }) => (
            <div key={n} className="text-center px-2">
              <div className="w-11 h-11 rounded-full bg-navy text-white font-extrabold text-[18px] flex items-center justify-center mx-auto mb-4">
                {n}
              </div>
              <h3 className="font-bold text-[18px] text-ink mb-1.5">
                {t[hKey]}
              </h3>
              <p className="text-muted text-[15px] leading-relaxed">{t[pKey]}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
