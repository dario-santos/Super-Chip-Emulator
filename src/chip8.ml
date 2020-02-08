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

(* VN: One of the 16 available variables. N may be 0 to F (hexadecimal)*)
let vn = Array.make 16 0

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

let clear_display () = 
    set_color (rgb 255 255 255);
    fill_rect 0 0 (truncate (64. *. 10.)) (truncate (32. *. 10.))
  
let clear_array a =
    Array.fill a 0 ((Array.length a) - 1) 0

let rec initialize () =

  (* Initialize the memory and registers *)
  clear_array key;
  clear_array vn;
  clear_array memory;

  stack := [];

  (* Load fontset *)
  for i = 0 to 79 do
    memory.(i) <- chip8_fontset.(i)
  done;

  (* Reset timers *)
	delay_timer := 0;
	sound_timer := 0

and cicle () =
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

and decode opcode =
    let oc  = opcode lsr 12 in 
    let x   = (opcode land 0x0F00) lsr 8 in
    let y   = (opcode land 0x00F0) lsr 4 in
    let c   = (opcode land 0x000F) lsr 2 in 
    let nn  = opcode land 0x00FF in
    let nnn = opcode land 0x0FFF in
    match oc, x, y, c with
    | 0x0, _, 0xE, 0xE -> (* Clears the screen *)  
      clear_display (); 
      pc := !pc + 2
    | 0x0, _, 0xE, _   -> assert false
    | 0x0, _, _, _ -> assert false
    | 0x3, _, _, _ ->
      pc := if x == nn then !pc + 4 else !pc + 2
    | 0x1, _, _, _ -> 
      pc := nnn
    | 0xA, _, _, _ -> 
      i := nnn;
      pc := !pc + 2
    | _ -> ()
  

exception Room of string

let load_file rom =
  initialize ();
  
  (* Load the ROM into RAM. *)
  let rom = open_in_bin rom in
  let rom_length = in_channel_length rom in
  if rom_length > 0xFFF - 0x200 + 1 then raise (Room "The given file is too big to be a CHIP-8 ROM.");
  
  for i = 0 to rom_length - 1 do
    memory.(0x200 + i) <- input_byte rom
  done;
  close_in rom