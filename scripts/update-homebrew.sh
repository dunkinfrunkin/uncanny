#!/usr/bin/env bash
# Generates/updates the homebrew formula for the dunkinfrunkin/homebrew-tap repo.
# Usage: ./scripts/update-homebrew.sh <version>
# Example: ./scripts/update-homebrew.sh 0.1.0

set -euo pipefail

VERSION="${1:?Usage: $0 <version>}"
REPO="dunkinfrunkin/uncanny"
TAP_REPO="dunkinfrunkin/homebrew-tap"

echo "Generating homebrew formula for uncanny v${VERSION}..."

# Get the tarball URL and sha256
TARBALL_URL="https://github.com/${REPO}/archive/refs/tags/v${VERSION}.tar.gz"
echo "Downloading ${TARBALL_URL}..."
SHA256=$(curl -sL "${TARBALL_URL}" | shasum -a 256 | cut -d' ' -f1)
echo "SHA256: ${SHA256}"

# Generate the formula
cat > /tmp/uncanny.rb << FORMULA
class Uncanny < Formula
  include Language::Python::Virtualenv

  desc "CLI tool that detects AI-generated text with sentence-level scoring"
  homepage "https://github.com/${REPO}"
  url "${TARBALL_URL}"
  sha256 "${SHA256}"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    virtualenv_install_with_resources
  end

  test do
    output = shell_output("#{bin}/uncanny version")
    assert_match "uncanny", output
  end
end
FORMULA

echo "Formula written to /tmp/uncanny.rb"
echo ""
echo "Next steps:"
echo "  1. Clone the tap repo: gh repo clone ${TAP_REPO}"
echo "  2. Copy the formula: cp /tmp/uncanny.rb Formula/uncanny.rb"
echo "  3. Commit and push"
echo ""
echo "Or push directly:"
echo "  gh api repos/${TAP_REPO}/contents/Formula/uncanny.rb \\"
echo "    -X PUT \\"
echo "    -f message='Add uncanny v${VERSION}' \\"
echo "    -f content=\$(base64 < /tmp/uncanny.rb)"
