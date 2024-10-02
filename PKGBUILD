# Maintainer: Roland Kiraly <rolandgyulakiraly at outlook dot com>

pkgname=nordlayer-bin
pkgver=3.3.1
pkgrel=1
pkgdesc="Proprietary VPN client for Linux"
arch=('x86_64')
url="https://nordlayer.com"
license=('custom:commercial')
replaces=('nordvpnteams-bin')
conflicts=('nordvpnteams-bin')
depends=('bash' 'libgcrypt' 'libgpg-error' 'libcap' 'hicolor-icon-theme' 'gmp' 'strongswan')
options=('!strip' '!emptydirs')
install="${pkgname}.install"
source=("https://downloads.nordlayer.com/linux/latest/debian/pool/main/nordlayer_3.3.1_amd64.deb")
sha512sums=('56054790a31894177b48837e9fb4dc95178b7f243f87a3a4bbab92729fc16387316df7cb1c21c58d852d2497eb75e9d124e09da0f116cf2b06841231b3823b14')

package() {
    cd "${srcdir}"
    ar x "nordlayer_${pkgver}_amd64.deb"
    tar -xzf data.tar.* -C "${pkgdir}"

    # Move sbin binaries to bin
    if [ -d "${pkgdir}/usr/sbin" ]; then
        mv "${pkgdir}/usr/sbin/"* "${pkgdir}/usr/bin"
        # Update the systemd service file to point to /usr/bin instead of /usr/sbin
        sed -i 's+/usr/sbin+/usr/bin+g' "${pkgdir}/usr/lib/systemd/system/nordlayer.service"
        # Remove the now-empty sbin directory
        rm -r "${pkgdir}/usr/sbin"
    fi
}
