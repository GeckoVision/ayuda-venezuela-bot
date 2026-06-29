import { Map, Users, BarChart3, Building2, Newspaper } from "lucide-react";

interface Props {
  t: Record<string, string>;
}

const ENDPOINTS = [
  {
    icon: Map,
    method: "GET",
    path: "/api/reports",
    descKey: "api_reports",
    color: "text-tg",
    bg: "bg-tg/10",
  },
  {
    icon: Users,
    method: "GET",
    path: "/api/persons/list",
    descKey: "api_persons",
    color: "text-blue",
    bg: "bg-blue/10",
  },
  {
    icon: BarChart3,
    method: "GET",
    path: "/api/persons/stats",
    descKey: "api_stats",
    color: "text-yellow",
    bg: "bg-yellow/10",
  },
  {
    icon: Building2,
    method: "GET",
    path: "/api/damage/recent",
    descKey: "api_damage",
    color: "text-red",
    bg: "bg-red/10",
  },
  {
    icon: Newspaper,
    method: "GET",
    path: "/api/news",
    descKey: "api_news",
    color: "text-muted",
    bg: "bg-surface",
  },
] as const;

export default function ApiEndpoints({ t }: Props) {
  return (
    <section className="py-14 md:py-16">
      <div className="mx-auto max-w-[920px] px-5">
        <h2 className="text-[clamp(22px,4vw,30px)] font-extrabold text-center tracking-tight mb-2 text-balance">
          {t.api_title}
        </h2>
        <p className="text-center text-muted max-w-[560px] mx-auto mb-9 text-pretty">
          {t.api_lead}
        </p>

        <div className="border border-line rounded-[16px] overflow-hidden bg-card divide-y divide-line">
          {ENDPOINTS.map(({ icon: Icon, method, path, descKey, color, bg }) => (
            <div
              key={path}
              className="flex items-start gap-4 px-5 py-4 hover:bg-surface/60 transition-colors"
            >
              <div
                className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5 ${bg}`}
              >
                <Icon size={17} className={color} aria-hidden="true" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2 mb-0.5">
                  <span className="text-[11px] font-bold bg-surface text-muted px-2 py-0.5 rounded font-mono">
                    {method}
                  </span>
                  <code className="text-[13px] font-mono text-ink font-semibold">
                    {path}
                  </code>
                </div>
                <p className="text-[13px] text-muted leading-relaxed">
                  {t[descKey]}
                </p>
              </div>
            </div>
          ))}
        </div>

        <p className="text-center text-[13px] text-muted mt-4">
          {t.api_note}{" "}
          <a
            href="https://sosvenezuela2026.com"
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-blue hover:underline"
          >
            sosvenezuela2026.com
          </a>
        </p>
      </div>
    </section>
  );
}
