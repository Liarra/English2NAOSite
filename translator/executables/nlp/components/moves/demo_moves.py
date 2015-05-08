from translator.executables.nlp.components.robot_commands import move_command

__author__ = 'NBUCHINA'

wave = move_command()
wave.params["move"] = """movem (
LHand, 0, 1000, 57, 1000, 0, 1000,
RHand, 0, 1000, 57, 1000, 0, 1000)"""
wave.tags = ["wave"]
wave.regexp = r"waves? .{0,20} (hand)?"

nod = move_command()
nod.params["move"] = """movem (
LHand, 0, 1000, 57, 1000, 0, 1000,
RHand, 0, 1000, 57, 1000, 0, 1000)"""
nod.tags = ["nod"]
nod.regexp = r"nodes? .{0,20} (head)?"

handshake = move_command()
handshake.params["move"] = """movem (
LHand, 0, 1000, 57, 1000, 0, 1000,
RHand, 0, 1000, 57, 1000, 0, 1000)"""
handshake.tags = ["shake", "hand", "make", "handshake",  "greet"]
wave.regexp = r"(shak(es?)|(ing).{0,20}( hand)?)|(mak(es?|ing).{0,20} handshake)"