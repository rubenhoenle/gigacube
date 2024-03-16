{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, treefmt-nix }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
      treefmtEval = treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
    in
    {
      formatter.${system} = treefmtEval.config.build.wrapper;
      checks.${system}.formatter = treefmtEval.config.build.check self;

      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          adafruit-ampy
        ];
        env = {
          AMPY_PORT = "/dev/ttyACM0";
        };
        shellHook = ''
          alias help="echo \"COMMANDS: deploy, reset, run\""
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
