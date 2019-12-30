with import <nixpkgs> {};

let
  python = python38;
  pythonPackages = python.pkgs;
  pyenv = (
  let
    microdata = pythonPackages.buildPythonPackage rec {
      name = "microdata-${version}";
      version = "0.6.1";
      src = fetchFromGitHub {
        owner = "edsu";
        repo = "microdata";
        rev = "refs/tags/v${version}";
        sha256 = "0vjli3x2mp46ky5givmhayl8ddd624w4w65bw6zg1chngrqg770q";
      };
      propagatedBuildInputs = with pythonPackages; [ html5lib ];
    };
    umpaumpa_ch = callPackage ./umpaumpa.nix {
      inherit pythonPackages;
    };
  in python.withPackages ( pypkgs: with pypkgs; [
    virtualenv 
    /* umpaumpa_ch */
  ])
);
in stdenv.mkDerivation {
  pname = "umpaumpa.ch-env";
  version = "1.0";
  buildInputs = with pkgs; [ pyenv gcc libffi libxml2 libxslt ];
}
