export const metadata = {
  title: 'Items — reference app',
  description: 'FastAPI + PostgreSQL + Next.js checkpoint',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
