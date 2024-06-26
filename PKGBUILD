# Maintainer: Roland Kiraly <rolandgyulakiraly at outlook dot com>
# https://github.com/raverecursion/nordlayer-latest/tree/master
pkgname=nordlayer
pkgver=3.2.2
pkgrel=4
pkgdesc="Proprietary VPN client for Linux"
arch=('x86_64')
url="https://nordlayer.com"
license=('custom:commercial')
replaces=('nordvpnteams-bin')
conflicts=('nordvpnteams-bin')
depends=('bash' 'libgcrypt' 'libgpg-error' 'libcap' 'hicolor-icon-theme' 'gmp')
options=('!strip' '!emptydirs')
install=${pkgname}.install
source_x86_64=("https://downloads.nordlayer.com/linux/latest/debian/pool/main/nordlayer_${pkgver}_amd64.deb")
sha512sums_x86_64=('f076ae853fb87941d1bc8c7cd34c31d233343a86b1d6b123353c328fda3fd938b7e38741ba1399f63eb2cdda990ddf460fde25e035eb810ea0c3d7de7e5303b2')

package() {
    cd "${srcdir}"
    # Extract the control and data tarballs from the .deb file
    ar x "${srcdir}/nordlayer_${pkgver}_amd64.deb"

    # Extract the data.tar.gz into the pkgdir
    tar -xzf data.tar.gz -C "${pkgdir}"

    # Move sbin binaries to bin
    if [ -d "${pkgdir}/usr/sbin" ]; then
        mv "${pkgdir}/usr/sbin"/* "${pkgdir}/usr/bin"
        # Update the systemd service file to point to /usr/bin instead of /usr/sbin
        sed -i 's+/usr/sbin+/usr/bin+g' "${pkgdir}/usr/lib/systemd/system/nordlayer.service"
        # Remove the now-empty sbin directory
        rm -r "${pkgdir}/usr/sbin"
    fi
}
