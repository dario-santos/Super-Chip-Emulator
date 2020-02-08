open Printf
open Graphics

let memory = Array.make 80 0

let chip8_fontset = [|
  0xF0; 0x90; 0x90; 0x90; 0xF0; (* 0 *)
  0x20; 0x60; 0x20; 0x20; 0x70; (* 1 *)
  0xF0; 0x10; 0xF0; 0x80; 0xF0; (* 2 *)
  0xF0; 0x10; 0xF0; 0x10; 0xF0; (* 3 *)
  0x90; 0x90; 0xF0; 0x10; 0x10; (* 4 *)
  0xF0; 0x80; 0xF0; 0x10; 0xF0; (* 5 *)
  0xF0; 0x80; 0xF0; 0x90; 0xF0; (* 6 *)
  0xF0; 0x10; 0x20; 0x40; 0x40; (* 7 *)
  0xF0; 0x90; 0xF0; 0x90; 0xF0; (* 8 *)
  0xF0; 0x90; 0xF0; 0x10; 0xF0; (* 9 *)
  0xF0; 0x90; 0xF0; 0x90; 0x90; (* A *)
  0xE0; 0x90; 0xE0; 0x90; 0xE0; (* B *)
  0xF0; 0x80; 0x80; 0x80; 0xF0; (* C *)
  0xE0; 0x90; 0x90; 0x90; 0xE0; (* D *)
  0xF0; 0x80; 0xF0; 0x80; 0xF0; (* E *)
  0xF0; 0x80; 0xF0; 0x80; 0x80  (* F *)
|]

(* Total memory *)
let memory = Array.make 4096 0

(* Register *)
let reg = Array.make 16 0

let key = Array.make 16 0

let stack : int list ref = ref []

let pc = ref 0x200
let opcode = ref 0
let i = ref 0
let sp = ref 0

(* Timers *)
let delay_timer = ref 0
let sound_timer = ref 0

exception Undefined of string
let error s = raise (Undefined s)

let decode opcode =
  let opcode = opcode land 0xF000 in 
  match opcode with 
  | 0xA000 -> 
    i := opcode land 0x0FFF;
    pc := !pc + 2
  | 0x8XY4 -> 
      

    if(V[(opcode & 0x00F0) >> 4] > (0xFF - V[(opcode & 0x0F00) >> 8]))
      V[0xF] = 1; //carry
    else
      V[0xF] = 0;
    V[(opcode & 0x0F00) >> 8] += V[(opcode & 0x00F0) >> 4];
    pc += 2; 
  | _ -> error ("Opcode " ^ string_of_int opcode ^ "not implemented.")


let clear_display () = 
  set_color (rgb 220 220 220);
  fill_rect 0 0 (truncate (64. *. 10.)) (truncate (32. *. 10.))

let clear_array a =
    Array.fill a 0 ((Array.length a) - 1) 0


let initialize () =

  (* Initialize the memory and registers *)
  clear_display ();
  clear_array key;
  clear_array reg;
  clear_array memory;

  stack := [];

  (* Load fontset *)
  for i = 0 to 79 do
    memory.(i) <- chip8_fontset.(i)
  done;

  (* Reset timers *)
	delay_timer := 0;
	sound_timer := 0

let cicle () =
  (* One emulation cicle *) 
      
  (* 1 - Fetch Opcode *)

  (*
    Merging two successive bytes to form the opcode

    memory.(!pc)     = 00000000 10100010
    memory.(!pc + 1) = 00000000 11110000

    a) shift the top 8 bits
    10100010 << 8    = 10100010 00000000

    b) merge the two bytes
    10100010 00000000 | 
    00000000 11110000
    -------------------
    10100010 11110000

  *)
  opcode := (memory.(!pc) lsl 8) lor memory.(!pc + 1);

  (* 
    Decode Opcode
    Execute Opcode
   *)
  ignore(decode !opcode);

  (* Update timers *)
  delay_timer := if !delay_timer > 0 then !delay_timer - 1 else !delay_timer;

  if !sound_timer > 0 then
    let _ = if !sound_timer = 1 then Graphics.sound 500 5000 else ();
  
    sound_timer := !sound_timer - 1
  in

  assert false 
