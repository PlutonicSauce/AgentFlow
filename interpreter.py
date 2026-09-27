import time

class Interpreter:
    def __init__(self):
        self.env = {}
        self.agents = {}
        self.flows = {}

    def interpret(self, ast):
        for stmt in ast.statements:
            self.execute(stmt)

    def execute(self, node, local_env=None):
        if local_env is None:
            local_env = self.env

        node_type = type(node).__name__

        if node_type == "AgentDecl":
            props = {k: self.evaluate(v, local_env) for k, v in node.props.items()}
            self.agents[node.name] = props
            print(f"[AgentFlow] Successfully compiled Agent: {node.name}")
            
        elif node_type == "FlowDecl":
            self.flows[node.name] = node
            print(f"[AgentFlow] Successfully compiled Flow: {node.name}")
            
        elif node_type == "RunStmt":
            print(f"\n[AgentFlow] Initiating Flow: '{node.name}'...")
            flow = self.flows.get(node.name)
            if not flow:
                raise Exception(f"Runtime Error: Flow '{node.name}' is not defined.")
            args = [self.evaluate(a, local_env) for a in node.args]
            self.call_flow(flow, args)
            
        elif node_type == "Assignment":
            val = self.evaluate(node.value, local_env)
            local_env[node.target] = val
            
        elif node_type == "MethodCall":
            return self.evaluate(node, local_env)

    def call_flow(self, flow_node, args):
        flow_env = {}
        for param, arg in zip(flow_node.params, args):
            flow_env[param] = arg
            
        return self.execute_block(flow_node.body, flow_env, flow_node.name)

    def execute_block(self, stmts, env, flow_name=None):
        last_val = None
        for stmt in stmts:
            stmt_type = type(stmt).__name__
            
            if stmt_type == "ReturnStmt":
                result = self.evaluate(stmt.value, env)
                if flow_name:
                    print(f"\n[AgentFlow] Flow '{flow_name}' completed. Result:\n--> {result}")
                return result
            else:
                last_val = self.execute(stmt, env)
        return last_val

    def evaluate(self, node, local_env):
        node_type = type(node).__name__
        
        if node_type == "RetryStmt":
            print(f"  [AgentFlow] 🛡️ Establishing retry block (max attempts: {node.count})")
            for attempt in range(1, node.count + 1):
                try:
                    result = self.execute_block(node.body, local_env)
                    return result
                except Exception as e:
                    print(f"  [AgentFlow] ⚠️ Attempt {attempt}/{node.count} failed. Retrying in 1s...")
                    time.sleep(1)
                    if attempt == node.count:
                        print(f"  [AgentFlow] ❌ Retry block exhausted after {node.count} attempts.")
                        raise e
        elif node_type == "StringLiteral":
            return node.value
        elif node_type == "NumberLiteral":
            return node.value
        elif node_type == "ListLiteral":
            return [self.evaluate(e, local_env) for e in node.elements]
            
        elif node_type == "Identifier":
            if node.name in local_env:
                return local_env[node.name]
            return node.name
            
        elif node_type == "MethodCall":
            if node.obj in self.agents and node.method == "run":
                agent = self.agents[node.obj]
                args = [self.evaluate(a, local_env) for a in node.args]
                return self.simulate_llm_call(node.obj, agent, args)
            else:
                raise Exception(f"Runtime Error: Unknown method '{node.method}' on object '{node.obj}'")

    def simulate_llm_call(self, agent_name, agent_props, args):
        print(f"\n  ┌── [ Agent: {agent_name} ]")
        print(f"  │ Model:  {agent_props.get('model', 'default')}")
        print(f"  │ Prompt: {agent_props.get('prompt', '')}")
        input_text = str(args[0]) if args else ""
        print(f"  │ Input:  {input_text}")
        print("  │ ⚙️ Thinking...")
        time.sleep(0.8)
        
        # Flaky mock implementation to show off the 'retry' feature
        if "flaky" in input_text.lower() and int(time.time() * 100) % 3 != 0:
            print("  │ ❌ Connection to LLM Provider lost!")
            print(f"  └── ✓ Failed")
            raise Exception("LLM Provider Timeout")

        lower_input = input_text.lower()
        if "summarize" in agent_props.get('prompt', '').lower() or "summary" in agent_props.get('prompt', '').lower():
            response = f"Brief overview: {input_text[:60]}..."
        elif "quantum" in lower_input:
            response = "Quantum computing relies on qubits, which exploit superposition and entanglement to perform complex calculations exponentially faster than classical computers."
        else:
            response = f"Processed knowledge regarding: {input_text}"
            
        print(f"  │ Output: {response}")
        print(f"  └── ✓ Complete")
        return response
