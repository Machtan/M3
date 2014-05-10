using UnityEngine;
using System.Collections;

public enum UpgradeSlot{
	Arms,
	Legs,
	Head,
	Eyes,
	Hands,
	Pants,
	Tail,
	Wings,
	Hat
}

public abstract class Upgrade {
	public UpgradeSlot slot;
	public string name;
	public string description;
	public Sprite appearance;

	public Upgrade(string name, UpgradeSlot slot, Sprite appearance, string description) {
		this.name = name;
		this.slot = slot;
		this.appearance = appearance;
		this.description = description;
	}

	public abstract void Start(); // Call when the game starts
	public abstract void Update(); // Call when the game updates
}
