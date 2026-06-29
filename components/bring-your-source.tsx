import { DatabaseZap, FileJson, Wrench, MessageCircle } from "lucide-react";

interface Props {
  t: Record<string, string>;
}

const PATHS = [
  {
    icon: FileJson,
    titleKey: "byos_path1_title",
    descKey: "byos_path1_desc",
    accent: "bg-blue/10 text-blue",
  },
  {
    icon: Wrench,
    titleKey: "byos_path2_title",
    descKey: "byos_path2_desc",
    accent: "bg-yellow/10 text-yellow",
  },
] as const;

export default function BringYourSource({ t }: Props) {
  return (
    <section className="py-14 md:py-16 bg-surface">
      <div className="mx-auto max-w-[920px] px-5">
        {/* Header */}
        <div className="text-center mb-10">
          <span className="inline-flex items-center gap-1.5 text-[13px] font-bold tracking-[1.2px] uppercase text-blue bg-blue/10 px-3 py-1.5 rounded-full mb-4">
            <DatabaseZap size={13} aria-hidden="true" />
            {t.byos_badge}
          </span>
          <h2 className="text-[clamp(22px,4vw,30px)] font-extrabold tracking-tight mb-3 text-balance">
            {t.byos_title}
          </h2>
          <p className="text-muted max-w-[580px] mx-auto leading-relaxed text-pretty">
            {t.byos_p}
          </p>
        </div>

        {/* Two-path cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
          {PATHS.map(({ icon: Icon, titleKey, descKey, accent }) => (
            <div
              key={titleKey}
              className="bg-card border border-line rounded-[16px] p-6 flex gap-4"
            >
              <div
                className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${accent}`}
              >
                <Icon size={20} aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-bold text-[16px] text-ink mb-1">
                  {t[titleKey]}
                </h3>
                <p className="text-muted text-[14px] leading-relaxed">
                  {t[descKey]}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* CTA row */}
        <div className="text-center flex flex-col items-center gap-4">
          <a
            href="https://github.com/GeckoVision/gecko-surf/issues/new"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2.5 font-bold px-6 py-3.5 rounded-full text-[16px] text-white transition-transform hover:-translate-y-px focus-visible:outline-2"
            style={{ background: "#2563eb" }}
          >
            {t.byos_cta}
          </a>
          <p className="text-[14px] text-muted flex items-center gap-1.5">
            <MessageCircle size={14} aria-hidden="true" />
            {t.byos_contact}{" "}
            <a
              href="https://x.com/ernanibritto"
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-ink hover:text-blue transition-colors"
            >
              X · @ernanibritto
            </a>
          </p>
        </div>
      </div>
    </section>
  );
}
