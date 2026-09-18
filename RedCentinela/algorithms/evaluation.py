import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)
    else:
        score = state.get_score()
        distancia_a_objetivo = float("inf")
        distancia_a_intruso = state.layout.distance(
        state.defender_position,
        state.intruder_position)

        for terminal in state.pending_terminals:
          distancia = state.layout.distance(
            state.defender_position,
            terminal
        )

          if distancia < distancia_a_objetivo:
            distancia_a_objetivo = distancia

        valor = score

        if distancia_a_objetivo != float("inf"):
          valor += 10 / (distancia_a_objetivo + 1)

        if distancia_a_intruso != float("inf"):
          valor -= 10 / (distancia_a_intruso + 1)

        acciones = state.get_legal_actions(0)
        valor += len(acciones)

        return max(-999, min(999, valor))


    # TODO: Add your code here
    return base_evaluation_function(state)

