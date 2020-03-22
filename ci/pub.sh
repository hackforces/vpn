# Publishing to yandex cloud
docker build -f ci/Dockerfile -t cr.yandex/crpnjr9i2f2ggh9opdjh/hf_vpn:latest .
docker push cr.yandex/crpnjr9i2f2ggh9opdjh/hf_vpn:latest

# Publishing to github
docker tag cr.yandex/crpnjr9i2f2ggh9opdjh/hf_vpn:latest docker.pkg.github.com/hackforces/vpn/vpn:latest
docker push docker.pkg.github.com/hackforces/vpn/vpn:latest