from Parser import Parser

"""
NOTE:

Repl is kinda useless, and broken, but i will fix it at a later date
ie. no variables will be remembered after each line so its really useless

"""
def repl(parser: Parser):
    print("""
███████╗ █████╗ ██████╗     ██████╗ ███████╗██████╗ ██╗     
╚══███╔╝██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██║     
  ███╔╝ ███████║██████╔╝    ██████╔╝█████╗  ██████╔╝██║     
 ███╔╝  ██╔══██║██╔═══╝     ██╔══██╗██╔══╝  ██╔═══╝ ██║     
███████╗██║  ██║██║         ██║  ██║███████╗██║     ███████╗
╚══════╝╚═╝  ╚═╝╚═╝         ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝
""")
    print("Zap REPL")
    print("Prototype Interpreter")
    print("Type 'exit' to leave the REPL")
    print("=" * 60)

    data: str = ""
    while True:
        code: str = input(">>> ")
        if code.lower() == "exit":
            print("=" * 60)
            print("Exiting ZAP REPL")
            print("-" * 60)
            print("Thanks for experimenting with Zap!")
            print("See you next time!")
            print("=" * 60)
            print("""
      ███████╗ █████╗ ██████╗ 
      ╚══███╔╝██╔══██╗██╔══██╗
        ███╔╝ ███████║██████╔╝
       ███╔╝  ██╔══██║██╔═══╝ 
      ███████╗██║  ██║██║     
      ╚══════╝╚═╝  ╚═╝╚═╝       
            """)
            break

        data += f"\n{code}"
        try:
            print(f"Debug: DAta: {data}")
            print(parser.parse(data).strip(data))
        except Exception as e:
            print(e)