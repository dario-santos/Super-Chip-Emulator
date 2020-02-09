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

(* Memory ram - 4KB*)
let memory = Array.make 4096 0

(* Registers: One of the 16 available variables.*)
let vn = Array.make 16 0

(* The Stack - Used for returns, normally has 48 bytes and 12 levels *)
let stack = Stack.create ()

(* Timers *)
let delay_timer = ref 0
let sound_timer = ref 0

let pc = ref 0x200
let opcode = ref 0
let i = ref 0

exception Undefined of string
let error s = raise (Undefined s)

let clear_display () = 
    set_color (rgb 255 255 255);
    fill_rect 0 0 (truncate (64. *. 10.)) (truncate (32. *. 10.))
  
let clear_array a = Array.fill a 0 ((Array.length a) - 1) 0

let rec initialize () =
  (* Clear the memory, registers and stack *)
  clear_array vn;
  clear_array memory;
  Stack.clear stack;

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

  (* 2 - Decode and Execute Opcode *)
  ignore(decode !opcode);

  (* 3 - Update timers *)
  delay_timer := if !delay_timer > 0 then !delay_timer - 1 else !delay_timer;

  if !sound_timer > 0 then
    let _ = if !sound_timer = 1 then Graphics.sound 500 5000 else ();
  
    sound_timer := !sound_timer - 1
    in
  ()

and decode opcode =
    let oc  = opcode lsr 12 in 
    let x   = (opcode land 0x0F00) lsr 8 in
    let y   = (opcode land 0x00F0) lsr 4 in
    let c   = (opcode land 0x000F) lsr 2 in 
    let nn  = opcode land 0x00FF in
    let nnn = opcode land 0x0FFF in
    match oc, x, y, c with
    | 0x0, 0x0, 0xE, 0x0 -> (* Clears the screen. *)  
      clear_display (); 
      pc := !pc + 2
    | 0x0, 0x0, 0xE, 0xE -> (* Returns from a subroutine. *)
      pc := Stack.pop stack;
    | 0x0, _, _, _ -> assert false
    | 0x1, _, _, _ -> (* Jumps to address NNN. *)
      pc := nnn
    | 0x2, _, _, _ -> (* Calls subroutine at NNN.*)
      Stack.push !pc stack;
      pc := nnn
    | 0x3, _, _, _ -> (* Skips the next instruction if VN(X) equals NN *)
      pc := if vn.(x) = nn then !pc + 4 else !pc + 2
    | 0x4, _, _, _ -> (* Skips the next instruction if VN(X) doesn't equal NN *)
      pc := if vn.(x) <> nn then !pc + 4 else !pc + 2
    | 0x5, _, _, 0x0 -> (* Skips the next instruction if VX equals VY. *)
      pc := if vn.(x) = vn.(y) then !pc + 4 else !pc + 2   
    | 0x6, _, _, _ -> (* Assigns the value of NN to VX. *)
      vn.(x) <- nn;
      pc := !pc + 2
    | 0x7, _, _, _ -> (* Adds NN to VX *)
      vn.(x) <- nn;
      pc := !pc + 2
    | 0x8, _, _, 0x0 -> (* Sets VX to the value of VY. *)
      vn.(x) <- vn.(y);
      pc := !pc + 2
    | 0x8, _, _, 0x1 -> (* Sets VX to VX or VY. (Bitwise OR operation) *)
      vn.(x) <- vn.(x) lor vn.(y);
      pc := !pc + 2
    | 0x8, _, _, 0x2 -> (* Sets VX to VX and VY. (Bitwise AND operation) *)
      vn.(x) <- vn.(x) land vn.(y);
      pc := !pc + 2
    | 0x8, _, _, 0x3 -> (* Sets VX to VX xor VY. (Bitwise XOR operation) *)
      vn.(x) <- vn.(x) lxor vn.(y);
      pc := !pc + 2
    | 0x8, _, _, 0x4 -> (* Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn't. *)
      vn.(x) <- vn.(x) + vn.(y);
      vn.(15) <- if (abs vn.(x)) > 9 then 1 else 0;
      pc := !pc + 2
    | 0x8, _, _, 0x5 -> (* VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't. *)
      vn.(15) <- if not (vn.(y) > vn.(x)) then 1 else 0;
      vn.(x) <- vn.(x) - vn.(y);
      pc := !pc + 2
    | 0x8, _, _, 0x6 -> (* Stores the least significant bit of VX in VF and then shifts VX to the right by 1. *)
      vn.(15) <- vn.(x) land 0x1; 
      vn.(x) <- vn.(x) lsr 1;
      pc := !pc + 2
    | 0x8, _, _, 0x7 -> (* Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't. *)
      vn.(15) <- if not (vn.(x) > vn.(y)) then 1 else 0;
      vn.(x) <- vn.(y) - vn.(x);
      pc := !pc + 2
    | 0x8, _, _, 0xE -> (* Stores the most significant bit of VX in VF and then shifts VX to the left by 1. *)
      vn.(15) <- vn.(x) land 0x80; 
      vn.(x) <- vn.(x) lsl 1;
      pc := !pc + 2
    | 0x9, _, _, 0x0 -> (* Skips the next instruction if VX doesn't equal VY. *)
      pc := if vn.(x) <> vn.(y) then !pc + 4 else !pc + 2
    | 0xA, _, _, _ -> (* Sets I to the address NNN. *)
      i := nnn;
      pc := !pc + 2
    | 0xB, _, _, _ -> (* Jumps to the address NNN plus V0. *)
      pc := vn.(0) + nnn
    | 0xC, _, _, _ -> (* Sets VX to the result of a bitwise and operation on a random number (Typically: 0 to 255) and NN. *)
      vn.(x) <- (Random.int 255) land nn;
      pc := !pc + 2
    | 0xD, _, _, _ -> (* Draws a sprite at coordinate (VX, VY). *)
      assert false
    | 0xE, _, 0x9, 0xE -> (* Skips the next instruction if the key stored in VX is pressed. *)
      pc := if (get_pressed_key ()) = vn.(x) then !pc + 4 else !pc + 2
    | 0xE, _, 0xA, 0x1 -> (* Skips the next instruction if the key stored in VX isn't pressed. *)
      pc := if (get_pressed_key ()) <> vn.(x) then !pc + 4 else !pc + 2
    | 0xF, _, 0x0, 0x7 -> (* Sets VX to the value of the delay timer. *)
      vn.(x) <- !delay_timer;
      pc := !pc + 2
    | 0xF, _, 0x0, 0xA -> assert false
    | 0xF, _, 0x1, 0x5 -> (* Sets the delay timer to VX. *)
      delay_timer := vn.(x);
      pc := !pc + 2
    | 0xF, _, 0x1, 0x8 -> (* Sets the sound timer to VX. *)
      sound_timer := vn.(x);
      pc := !pc + 2
    | 0xF, _, 0x1, 0xE -> (* Adds VX to I. VF is set to 1 when there is a range overflow 0 otherwise. *)
      vn.(15) <- if !i + vn.(x) > 0xFFF then 1 else 0;
      i := !i + vn.(x); 
      pc := !pc + 2
    | 0xF, _, 0x2, 0x9 -> assert false
    | 0xF, _, 0x3, 0x3 -> assert false
    | 0xF, _, 0x5, 0x5 -> assert false
    | 0xF, _, 0x6, 0x5 -> assert false
    | _ -> raise (Undefined "Error, opcode undefined.")

and get_pressed_key () =
  if not (key_pressed ()) then -1 else
  match (read_key ()) with  
  | '1' -> 0
  | '2' -> 1
  | '3' -> 2
  | '4' -> 3
  | 'Q' -> 4
  | 'W' -> 5
  | 'E' -> 6
  | 'R' -> 7
  | 'A' -> 8
  | 'S' -> 9
  | 'D' -> 10
  | 'F' -> 11
  | 'Z' -> 12
  | 'X' -> 13
  | 'C' -> 14
  | 'V' -> 15
  | _ -> -1

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