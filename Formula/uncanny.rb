class Uncanny < Formula
  include Language::Python::Virtualenv

  desc "CLI tool that detects AI-generated text with sentence-level scoring"
  homepage "https://github.com/dunkinfrunkin/uncanny"
  url "https://github.com/dunkinfrunkin/uncanny/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "" # TODO: fill after first release
  license "MIT"

  depends_on "python@3.12"

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.24.1.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.3.3.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/source/c/click/click-8.3.1.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/source/m/markdown-it-py/markdown_it_py-4.0.0.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/source/m/mdurl/mdurl-0.1.2.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.19.2.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  resource "shellingham" do
    url "https://files.pythonhosted.org/packages/source/s/shellingham/shellingham-1.5.4.tar.gz"
    sha256 "" # TODO: fill from PyPI
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    output = shell_output("#{bin}/uncanny version")
    assert_match "uncanny", output

    output = shell_output("#{bin}/uncanny scan --text 'Hello world' --format summary")
    assert_match(/\d+\.\d+/, output)
  end
end
