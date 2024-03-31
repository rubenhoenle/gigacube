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

      emulator = {
        
        Gigacube = pkgs.python39.pkgs.buildPythonPackage rec {
          pname = "gigacube";
          version = "1.0";

          src = ./faradaycage/gigacubeLibary;

          buildInputs = with pkgs.python39Packages; [
            setuptools
            wheel
            pygame
            pyopengl
          ];
      };
        
        NeoPixel = pkgs.python39.pkgs.buildPythonPackage rec {
          pname = "neopixel";
          version = "1.0";

          src = ./faradaycage/neopixelLibary;

          buildInputs = with pkgs.python39Packages; [
            setuptools
            wheel
            emulator.Gigacube
            pygame
            pyopengl
          ];
      };

      Machine = pkgs.python39.pkgs.buildPythonPackage rec {
          pname = "machine";
          version = "1.0";

          src = ./faradaycage/machineLibary;

          buildInputs = with pkgs.python39Packages; [
            setuptools
            wheel
          ];
      };
    };

    in
    {
      formatter.${system} = treefmtEval.config.build.wrapper;
      checks.${system}.formatter = treefmtEval.config.build.check self;

      devShells.${system} = {
        
        default = pkgs.mkShell {
      
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
      
      faradaycage = pkgs.mkShell {
        packages = [
              pkgs.python3
        ];
        buildInputs = [emulator.NeoPixel
                      emulator.Machine
                      emulator.Gigacube

                      # for developing the Visulizier
                      pkgs.python3Packages.pygame
                      pkgs.python3Packages.numpy
                      pkgs.python39Packages.pyopengl
                      ];

        env = {
          #AMPY_PORT = "/dev/ttyACM0";
        };
        shellHook = ''
          echo Safe from any electrical Fields

          export PYTHONPATH="${emulator.NeoPixel}/lib/python3.9/site-packages:$PYTHONPATH"
          export PYTHONPATH="${emulator.Machine}/lib/python3.9/site-packages:$PYTHONPATH"
          export PYTHONPATH="${emulator.Gigacube}/lib/python3.9/site-packages:$PYTHONPATH"
          export PYTHONPATH="${pkgs.python3Packages.pygame}/lib/python3.9/site-packages:$PYTHONPATH"
          export PYTHONPATH="${pkgs.python3Packages.numpy}/lib/python3.9/site-packages:$PYTHONPATH"
          export PYTHONPATH="${pkgs.python39Packages.pyopengl}/lib/python3.9/site-packages:$PYTHONPATH"
        '';
      };
      };

    };
}
