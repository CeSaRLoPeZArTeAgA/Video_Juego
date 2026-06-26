# Pollo Multiverso: Las Vueltas del Destino

Juego arcade en Pygame basado en el tema:

> La vida da vueltas como pollito a la brasa ...............te toca sobrevivir a todo.

El proyecto mantiene una estructura modular similar al juego base Galaga: pantallas, jugador, enemigos, balas, colisiones, puntaje, estado y assets separados en carpetas.

## Universos

1. **Polleria Espacial**  
   Tipo Galaga. El pollo dispara aji laser contra brasas espaciales, papas alienigenas y gaseosas flotantes.  
   Jefe: **El Cometa Brasa**.

2. **Universidad del Pollo**  
   Recolecta libros y evita parciales, tareas y el grupo que abandono.  
   Jefe: **El Examen Final de Grafica 3 horas**.

3. **Delivery Infernal**  
   Carrera lateral. Salta huecos, esquiva motos, tickets y clientes hambrientos.  
   Jefe: **El Motorizado Supremo**.

4. **Oficina del Pollo Adulto**  
   Evita recibos, deudas, correos, reuniones y trafico. Recolecta cafe, dinero y descanso.  
   Jefe: **El Pago de Fin de Mes**.

## Controles

- Flechas o WASD: mover el pollo.
- SPACE: disparar en universos 1, 2 y 4.
- SPACE: saltar en Delivery Infernal.
- J: disparar en cualquier universo, especialmente en Delivery Infernal.
- P: pausar.
- ESC: salir.
- R: reiniciar desde la pantalla final.

## Ejecucion

```bash
python -m pip install -r requirements.txt
python main.py
```

En Windows tambien puedes usar:

```bat
run.bat
```

## Estructura

```text
pollo_multiverso_vueltas_destino/
├── main.py
├── screenManager.py
├── screenMain.py
├── screenGame.py
├── screenResult.py
├── player.py
├── bullet.py
├── bulletManager.py
├── bulletType.py
├── enemy.py
├── enemyBomb.py
├── enemySpawner.py
├── collisionDetector.py
├── boss.py
├── background.py
├── powerUp.py
├── score.py
├── status.py
├── universes.py
├── utils.py
├── config.py
├── imagenes/
│   ├── Player/
│   ├── Bullets/
│   ├── Enemies/
│   ├── Bosses/
│   ├── Powerups/
│   ├── Backgrounds/
│   └── UI/
├── requirements.txt
└── run.bat
```

## Como modificar el juego

- Cambiar vidas, pantalla o FPS: `config.py`.
- Cambiar los universos, frases, objetivos, enemigos y jefes: `universes.py`.
- Cambiar imagenes: carpeta `imagenes/`.
- Cambiar controles o movimiento: `player.py`.
- Cambiar reglas generales de partida: `screenGame.py`.


## Mejoras de esta version

- Se agrego audio: musica por universo y efectos de salto, disparo, golpe, power-up, jefe, portal, victoria y derrota.
- Se ajusto Delivery Infernal para que sea mas claro y mas pasable: ahora tiene salto doble, mas espacio horizontal, menos castigo, auto-disparo contra el jefe y una ayuda visual en pantalla.
- Se mejoro el tratamiento visual de sprites y fondos con un realce de color, contraste y nitidez.
