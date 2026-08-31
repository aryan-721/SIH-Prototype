import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI-Enabled Skill Intelligence & Personalized Learning Platform | MoSPI NSSTA',
  description: 'Government enterprise competency intelligence, transparent skill-gap scoring, grounded RAG recommendations, and career navigator.',
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
