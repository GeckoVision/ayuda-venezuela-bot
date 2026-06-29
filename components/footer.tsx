interface Props {
  t: Record<string, string>;
}

export default function Footer({ t }: Props) {
  const links = [
    { label: "Telegram", href: "https://t.me/DEV_VEZbot" },
    { label: "GitHub", href: "https://github.com/GeckoVision/surfcall" },
    { label: "Build4Venezuela", href: "https://build4venezuela.com" },
    { label: t.footer_contact, href: "https://x.com/ernanibritto" },
  ];

  return (
    <footer className="bg-navy text-subtle py-9 text-center text-[14px]">
      <div className="mx-auto max-w-[920px] px-5">
        {/* Nav links */}
        <nav className="flex flex-wrap gap-x-5 gap-y-2 justify-center mb-4">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-white font-semibold hover:underline"
            >
              {l.label}
            </a>
          ))}
        </nav>

        {/* Builders strip */}
        <p className="text-subtle mb-3 max-w-[600px] mx-auto leading-relaxed">
          {t.builders}
        </p>

        {/* Disclaimer */}
        <p className="text-red font-semibold mb-3">{t.footer_disc}</p>

        {/* Made by */}
        <p className="text-subtle/70">{t.footer_made}</p>
      </div>
    </footer>
  );
}
