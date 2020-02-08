CMO= chip8.cmo main.cmo
GENERATED= chip8.cmi
BIN=chip8
FLAGS=

all: $(BIN)
	./$(BIN)
	
$(BIN):$(CMO)
	ocamlc $(FLAGS) -o $(BIN) graphics.cma $(CMO)

.SUFFIXES: .mli .ml .cmi .cmo .mll .mly

.mli.cmi:
	ocamlc $(FLAGS) -c  $<

.ml.cmo:
	ocamlc $(FLAGS) -c $<

clean:
	rm -f *.cm[io] *.o *~ $(BIN) $(GENERATED) 
	
.depend depend:$(GENERATED)
	rm -f .depend
	ocamldep *.ml *.mli > .depend

include .depend
