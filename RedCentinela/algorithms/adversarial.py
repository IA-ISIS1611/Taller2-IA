from abc import ABC, abstractmethod

from algorithms.evaluation import evaluation_function
from world.game_state import GameState


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        self.nodes_evaluated = 0

        def minValue(state, plies):
          self.nodes_evaluated +=1

          #Revisar si un estado es terminal o si se alcanza el limite de profundidad
          if state.is_win() or state.is_lose() or plies == 0: 
            return evaluation_function(state), None
    
          #Inicializa el valor minimo como infinito porque estamos buscando valores mas pequeños
          min_value = float('inf')
          best_action = None

          #Como estamos en un nodo min, sabemos que el agente es el intruso, entonces agent_index = 1
          actions = state.get_legal_actions(1)
          for action in actions: 
            #Generamos los sucesores del estado actual dada una acción
            successor = state.generate_successor(1, action)
            #Calculamos el valor del siguiente nodo y reducimos los plies
            current_value = maxValue(successor, plies-1)[0]

            #Si el valor del sucesor es estrictamente menor que el actual entonces actualizamos
            if current_value < min_value: 
                min_value = current_value
                best_action = action
          return min_value, best_action

        def maxValue(state, plies):
          self.nodes_evaluated +=1
          
          #Revisar si un estado es terminal o si se alcanza el limite de profundidad
          if state.is_win() or state.is_lose() or plies == 0: 
            return evaluation_function(state), None
    
          #Inicializa el valor maximo como menos infinito porque estamos buscando valores mas pequeños
          max_value = float('-inf')
          best_action = None

          #Como estamos en un nodo max, sabemos que el agente es el defensor, entonces agent_index = 0
          actions = state.get_legal_actions(0)
          for action in actions: 
            #Generamos los sucesores del estado actual dada una acción
            successor = state.generate_successor(0, action)
            #Calculamos el valor del siguiente nodo y reducimos los plies
            current_value = minValue(successor, plies-1)[0]

            #Si el valor del sucesor es estrictamente mayor que el actual entonces actualizamos
            if current_value > max_value: 
                max_value = current_value
                best_action = action
          return max_value, best_action
        

        #Empezamos en un nodo max (turno del defensor)
        action = maxValue(state, self.depth)[1]
        return action
        #raise NotImplementedError("Punto 4: implemente MinimaxAgent.get_action")


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción de Minimax aplicando poda alfa-beta.

        Debe usar la misma profundidad, orden de acciones y función de
        evaluación que Minimax.

        Tips:
        - Conserve la misma estructura y casos base de MinimaxAgent.
        - Inicie alpha en -infinito y beta en +infinito, y páselos en las
          llamadas recursivas.
        - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
          y corte si valor <= alpha.
        """

        self.nodes_evaluated = 0

        def minValue(state, plies, alpha, beta):
            self.nodes_evaluated += 1

            if state.is_win() or state.is_lose() or plies == 0:
                return evaluation_function(state), None

            min_value = float('inf')
            best_action = None

            actions = state.get_legal_actions(1)

            for action in actions:
                successor = state.generate_successor(1, action)
                current_value = maxValue(
                    successor,
                    plies - 1,
                    alpha,
                    beta
                )[0]

                if current_value < min_value:
                    min_value = current_value
                    best_action = action

                if min_value <= alpha:
                    break

                beta = min(beta, min_value)

            return min_value, best_action


        def maxValue(state, plies, alpha, beta):
            self.nodes_evaluated += 1

            if state.is_win() or state.is_lose() or plies == 0:
                return evaluation_function(state), None

            max_value = float('-inf')
            best_action = None

            actions = state.get_legal_actions(0)

            for action in actions:
                successor = state.generate_successor(0, action)
                current_value = minValue(
                    successor,
                    plies - 1,
                    alpha,
                    beta
                )[0]

                if current_value > max_value:
                    max_value = current_value
                    best_action = action

                if max_value >= beta:
                    break

                alpha = max(alpha, max_value)

            return max_value, best_action


        alpha = float('-inf')
        beta = float('inf')

        action = maxValue(state, self.depth, alpha, beta)[1]

        return action

"""
class AlphaBetaAgent(MultiAgentSearchAgent):
    #Agente Minimax que evita explorar ramas mediante poda alfa-beta.

    def get_action(self, state: GameState) -> str | None:
        
        alpha = float("-inf")
        beta = float("inf")

        best_value = float("-inf")
        best_action = None

        for action in state.get_legal_actions(0):
            successor = state.generate_successor(0, action)

            value = self.min_value(
                successor, 0, 1, alpha, beta
            )

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

        return best_action

    def max_value(self, state, depth, alpha, beta):

        if depth == self.depth or state.is_win() or state.is_lose():
            return evaluation_function(state)

        value = float("-inf")

        for action in state.get_legal_actions(0):
            successor = state.generate_successor(0, action)

            value = max(
                value,
                self.min_value(
                    successor, depth, 1, alpha, beta
                )
            )

            alpha = max(alpha, value)

            if value >= beta:
                break

        return value

    def min_value(self, state, depth, agent, alpha, beta):

        if depth == self.depth or state.is_win() or state.is_lose():
            return evaluation_function(state)

        value = float("inf")

        for action in state.get_legal_actions(agent):
            successor = state.generate_successor(agent, action)

            if agent == state.get_num_agents() - 1:
                value = min(
                    value,
                    self.max_value(
                        successor, depth + 1, alpha, beta
                    )
                )
            else:
                value = min(
                    value,
                    self.min_value(
                        successor, depth, agent + 1, alpha, beta
                    )
                )

            beta = min(beta, value)

            if value <= alpha:
                break

        return value
        # TODO: Add your code here
        raise NotImplementedError("Punto 5: implemente AlphaBetaAgent.get_action")
"""

