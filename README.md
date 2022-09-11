# System 0

The “Thinking, Fast and Slow” paradigm of Kahneman proposes that we use two different styles of thinking—a fast and intuitive System 1 for certain tasks, along with a slower but more logical System 2 for others. We consider how to interleave these two styles of thinking, i.e., we to decide whether System 1 or System 2 will do best. For this, we propose a System 0 that works along with Systems
1 and 2. At every point when a decision needs to be made, it evaluates the situation and quickly hands
over the decision making process to either System 1 or System 2. 

We have evaluated this framework using the classic arcade game Pac-Man. The environment used is based on the one used for [CS 188](http://ai.berkeley.edu/home.html) at UC Berkeley. We have created agents that mimic the behaviour of System 1 and System 2. In addition, we have proposed various systems that can be used as System 0. These have been defined in the file [3\_system\_agents.py](https://github.com/gulu42/System-0/blob/master/3_system_agents.py). More details can be found [here](https://arxiv.org/abs/2010.16244).

Experiments can be run using the file [pacman.py](https://github.com/gulu42/System-0/blob/master/pacman.py). For example, if you want to run the *proximity agent* using System 2 as the escape system with a proximity distance of 2 for 2000 games on *smallClassic* layout against *directional ghosts*  run the command:

```
python pacman.py -p ProximityAgent -n 2000 -a proxi_dist=2,escape_sys=2 -q -g DirectionalGhost -l smallClassic
```

If you have any questions, feel free to reach out to [me](https://gulu42.github.io/).

