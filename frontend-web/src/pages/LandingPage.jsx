/**
 * Landing Page Component
 * 
 * Minimalistic, chemistry-themed landing page for Reactometrix.
 * Inspired by modern SaaS design with the brand's sage/forest green palette.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  // If already logged in, go straight to dashboard
  if (isAuthenticated()) {
    navigate('/dashboard', { replace: true });
    return null;
  }

  return (
    <div className="landing">
      {/* ── Navigation Bar ── */}
      <nav className="landing-nav">
        <div className="landing-nav-inner">
          <div className="landing-brand">
            <svg
              width="36"
              height="36"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M 26 8 L 26 20 L 18 38 Q 16 42, 18 46 L 46 46 Q 48 42, 46 38 L 38 20 L 38 8"
                stroke="var(--color-forest)"
                strokeWidth="2.5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <line x1="26" y1="8" x2="38" y2="8" stroke="var(--color-forest)" strokeWidth="2.5" strokeLinecap="round" />
              <circle cx="32" cy="24" r="2.5" fill="var(--color-forest)" />
              <circle cx="24" cy="30" r="2.5" fill="var(--color-forest)" />
              <circle cx="32" cy="32" r="2.5" fill="var(--color-forest)" />
              <circle cx="40" cy="30" r="2.5" fill="var(--color-forest)" />
              <circle cx="22" cy="38" r="2.5" fill="var(--color-forest)" />
              <circle cx="30" cy="40" r="2.5" fill="var(--color-forest)" />
              <circle cx="34" cy="40" r="2.5" fill="var(--color-forest)" />
              <circle cx="42" cy="38" r="2.5" fill="var(--color-forest)" />
              <line x1="32" y1="24" x2="24" y2="30" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="32" y1="24" x2="32" y2="32" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="32" y1="24" x2="40" y2="30" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="24" y1="30" x2="32" y2="32" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="40" y1="30" x2="32" y2="32" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="24" y1="30" x2="22" y2="38" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="32" y1="32" x2="30" y2="40" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="32" y1="32" x2="34" y2="40" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="40" y1="30" x2="42" y2="38" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="22" y1="38" x2="30" y2="40" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="30" y1="40" x2="34" y2="40" stroke="var(--color-forest)" strokeWidth="1.8" />
              <line x1="34" y1="40" x2="42" y2="38" stroke="var(--color-forest)" strokeWidth="1.8" />
            </svg>
            <span className="landing-brand-name">Reactometrix</span>
          </div>
          <div className="landing-nav-actions">
            <button className="btn btn-ghost" onClick={() => navigate('/login')}>
              Log in
            </button>
            <button className="btn btn-primary" onClick={() => navigate('/register')}>
              Get started free
            </button>
          </div>
        </div>
      </nav>

      {/* ── Hero Section ── */}
      <section className="landing-hero">
        <div className="landing-hero-inner">
          <span className="landing-badge">Built for Chemical Engineers</span>
          <h1 className="landing-headline">
            Visualize equipment data.<br />
            <span className="landing-headline-accent">Make smarter decisions.</span>
          </h1>
          <p className="landing-subheadline">
            Upload CSV datasets, explore interactive charts, and generate professional 
            PDF reports — all in one streamlined platform designed for chemical equipment analysis.
          </p>
          <div className="landing-hero-actions">
            <button className="btn btn-primary btn-lg" onClick={() => navigate('/register')}>
              Start for free
            </button>
            <button className="btn btn-secondary btn-lg" onClick={() => navigate('/login')}>
              Sign in
            </button>
          </div>
        </div>

        {/* Decorative molecular background */}
        <div className="landing-hero-bg" aria-hidden="true">
          <svg width="100%" height="100%" viewBox="0 0 800 400" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
            {/* Subtle molecular bonds */}
            <circle cx="120" cy="80" r="6" fill="var(--color-forest)" opacity="0.07" />
            <circle cx="200" cy="140" r="4" fill="var(--color-forest)" opacity="0.05" />
            <line x1="120" y1="80" x2="200" y2="140" stroke="var(--color-forest)" strokeWidth="1" opacity="0.05" />
            
            <circle cx="650" cy="60" r="5" fill="var(--color-forest)" opacity="0.06" />
            <circle cx="720" cy="120" r="8" fill="var(--color-forest)" opacity="0.04" />
            <circle cx="580" cy="100" r="3" fill="var(--color-forest)" opacity="0.07" />
            <line x1="650" y1="60" x2="720" y2="120" stroke="var(--color-forest)" strokeWidth="1" opacity="0.04" />
            <line x1="580" y1="100" x2="650" y2="60" stroke="var(--color-forest)" strokeWidth="1" opacity="0.04" />

            <circle cx="100" cy="320" r="7" fill="var(--color-forest)" opacity="0.05" />
            <circle cx="180" cy="280" r="4" fill="var(--color-forest)" opacity="0.06" />
            <line x1="100" y1="320" x2="180" y2="280" stroke="var(--color-forest)" strokeWidth="1" opacity="0.04" />

            <circle cx="700" cy="300" r="5" fill="var(--color-forest)" opacity="0.06" />
            <circle cx="750" cy="350" r="3" fill="var(--color-forest)" opacity="0.05" />
            <line x1="700" y1="300" x2="750" y2="350" stroke="var(--color-forest)" strokeWidth="1" opacity="0.04" />

            <circle cx="400" cy="350" r="4" fill="var(--color-forest)" opacity="0.04" />
            <circle cx="350" cy="380" r="6" fill="var(--color-forest)" opacity="0.03" />
            <line x1="400" y1="350" x2="350" y2="380" stroke="var(--color-forest)" strokeWidth="1" opacity="0.03" />
          </svg>
        </div>
      </section>

      {/* ── Features Section ── */}
      <section className="landing-features">
        <div className="landing-features-inner">
          <h2 className="landing-section-title">Everything you need to analyze chemical data</h2>
          <p className="landing-section-subtitle">
            A complete toolkit from upload to report — no complexity, just clarity.
          </p>

          <div className="landing-features-grid">
            {/* Feature 1 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
              </div>
              <h3 className="landing-feature-title">CSV Upload</h3>
              <p className="landing-feature-desc">
                Drag and drop your equipment data files. We parse and organize them instantly so you can focus on analysis.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10" />
                  <line x1="12" y1="20" x2="12" y2="4" />
                  <line x1="6" y1="20" x2="6" y2="14" />
                </svg>
              </div>
              <h3 className="landing-feature-title">Interactive Charts</h3>
              <p className="landing-feature-desc">
                Bar charts, pie charts, and parameter comparisons — all interactive and rendered in real time from your data.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
              </div>
              <h3 className="landing-feature-title">PDF Reports</h3>
              <p className="landing-feature-desc">
                Generate professional, print-ready PDF reports with a single click. Share findings with your team instantly.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <h3 className="landing-feature-title">Dataset History</h3>
              <p className="landing-feature-desc">
                Every upload is saved securely. Browse, compare, and revisit past datasets whenever you need them.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="14" y="14" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                </svg>
              </div>
              <h3 className="landing-feature-title">Summary Dashboard</h3>
              <p className="landing-feature-desc">
                Get a clear overview of equipment counts, parameter ranges, and key metrics at a glance on one unified dashboard.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="landing-feature-card">
              <div className="landing-feature-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
              </div>
              <h3 className="landing-feature-title">Secure & Private</h3>
              <p className="landing-feature-desc">
                Token-based authentication keeps your data safe. Each user sees only their own datasets and reports.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── How It Works Section ── */}
      <section className="landing-how">
        <div className="landing-how-inner">
          <h2 className="landing-section-title">Up and running in 3 steps</h2>
          <div className="landing-steps">
            <div className="landing-step">
              <div className="landing-step-number">1</div>
              <h3>Create an account</h3>
              <p>Sign up in seconds — no credit card, no setup hassle.</p>
            </div>
            <div className="landing-step-divider" />
            <div className="landing-step">
              <div className="landing-step-number">2</div>
              <h3>Upload your CSV</h3>
              <p>Drop your equipment data file and let Reactometrix do the heavy lifting.</p>
            </div>
            <div className="landing-step-divider" />
            <div className="landing-step">
              <div className="landing-step-number">3</div>
              <h3>Explore & export</h3>
              <p>Interact with charts, review summaries, and download PDF reports.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA Section ── */}
      <section className="landing-cta">
        <div className="landing-cta-inner">
          <h2>Ready to simplify your equipment analysis?</h2>
          <p>Join engineers who trust Reactometrix to turn raw data into clear insights.</p>
          <button className="btn btn-primary btn-lg" onClick={() => navigate('/register')}>
            Get started — it's free
          </button>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="landing-footer">
        <div className="landing-footer-inner">
          <div className="landing-footer-brand">
            <svg
              width="24"
              height="24"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M 26 8 L 26 20 L 18 38 Q 16 42, 18 46 L 46 46 Q 48 42, 46 38 L 38 20 L 38 8"
                stroke="var(--color-gray-400)"
                strokeWidth="2.5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <line x1="26" y1="8" x2="38" y2="8" stroke="var(--color-gray-400)" strokeWidth="2.5" strokeLinecap="round" />
            </svg>
            <span>Reactometrix</span>
          </div>
          <p className="landing-footer-copy">
            &copy; {new Date().getFullYear()} Reactometrix &mdash; Chemical Equipment Parameter Visualizer
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
