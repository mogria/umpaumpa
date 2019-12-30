{ pythonPackages }:

pythonPackages.buildPythonPackage rec {
  name = "umpaumpa.ch";
  src = ./.;
  navtiveBuildInputs = with pythonPackages; [
    pytest
  ];
  propagatedBuildInputs = with pythonPackages; [
    django
    microdata
    scrapy
    dateutil
  ];
}
