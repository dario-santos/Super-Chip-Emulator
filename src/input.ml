open Sdl.Event

let input_scheme = [| 
  Sdlscancode.Num1;   (* 1 - 0x0 *)
  Sdlscancode.Num2;   (* 2 - 0x1 *)
  Sdlscancode.Num3;   (* 3 - 0x2 *)
  Sdlscancode.Num4;   (* 4 - 0x3 *)
  
  Sdlscancode.Q;      (* A - 0x4 *)
  Sdlscancode.W;      (* S - 0x5 *)
  Sdlscancode.E;      (* D - 0x6 *)
  Sdlscancode.R;      (* F - 0x7 *)

  Sdlscancode.A;      (* A - 0x8 *)
  Sdlscancode.B;      (* S - 0x9 *)
  Sdlscancode.C;      (* D - 0xA *)
  Sdlscancode.F;      (* F - 0xB *)

  Sdlscancode.Z;      (* Z - 0xC *)
  Sdlscancode.X;      (* X - 0xD *)
  Sdlscancode.C;      (* C - 0xE *)
  Sdlscancode.V;      (* V - 0xF *)
|]

let is_key_pressed keycode = 
  if keycode < 0x0 or keycode > 0xF then false 
  else Sdlkey.is_key_pressed (Array.get keycode)
