open Chip8
open Graphics

let screen_width  = 64.
let screen_height = 32.

let modifier = 10.

(* Window size *)
let display_width  = screen_width *. modifier
let display_height = screen_height *. modifier

let setup_graphics () =
  let s = Printf.sprintf " %dx%d" (truncate display_width) (truncate display_height) in
  open_graph s;
  auto_synchronize false

let main () =  
  (* Setup graphics and Input*)

  (*

  setupInput ()

  initialize Chip8 system and load the game

  *)
  Chip8.load_file "pong2.c8";
  setup_graphics ();

  (* Emulation Loop *)

  while true do
    (* Emulate one cicle *)
    Chip8.cicle ();
    
    (* Update graphics *)
    (* See if the player is pressing any key *)
    ()
  done;
  0

let _ = main ()
