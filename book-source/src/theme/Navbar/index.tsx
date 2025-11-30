import React from 'react';
import Navbar from '@theme-original/Navbar';
import type NavbarType from '@theme/Navbar';
import type {WrapperProps} from '@docusaurus/types';
import NavbarAuth from '../../components/NavbarAuth/NavbarAuth';

type Props = WrapperProps<typeof NavbarType>;

export default function NavbarWrapper(props: Props): React.ReactElement {
  return (
    <>
      <Navbar {...props} />
      <style>{`
        .navbar__items--right {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .navbar-auth-container {
          position: fixed;
          top: 0;
          right: 160px;
          height: var(--ifm-navbar-height);
          display: flex;
          align-items: center;
          z-index: 1000;
        }
        @media (max-width: 996px) {
          .navbar-auth-container {
            right: 80px;
          }
        }
        @media (max-width: 767px) {
          .navbar-auth-container {
            right: 10px;
            position: absolute;
          }
          /* Hide the logo and title from showing in doc sidebar area */
          .navbar-sidebar .navbar__brand {
            display: none;
          }
        }
      `}</style>
      <div className="navbar-auth-container">
        <NavbarAuth />
      </div>
    </>
  );
}
