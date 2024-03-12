{
  description = "A very basic flake";

  outputs = { self, nixpkgs }: 
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        adafruit-ampy
        jdk21
        gradle
      ];
      env = {
        AMPY_PORT = "/dev/ttyACM0";
      };
      shellHook = ''
        alias deploy="ampy put lib && ampy put webserver.py"
        alias reset="ampy reset"
        alias run="ampy run main.py"
        alias npmCi="ampy put lib && ampy put webserver.py"
        alias cleanEclipse="ampy reset"
        alias buildCommand="ampy run main.py"
      '';
    }; 

  };
}
