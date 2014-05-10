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

public class Upgrade {
	public UpgradeSlot slot;
	public string name;
	public string description;
	public Sprite appearance;
	protected GameObject target;
	protected GameObject component;
	protected Transform transform;

	public void Init(string name, UpgradeSlot slot, string texture, string description) {
		this.name = name;
		this.slot = slot;
		Texture2D tex = (Texture2D)Resources.Load (texture);
		Debug.Log ("The texture is "+tex);
		appearance = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), Vector2.zero);
		Debug.Log ("Appearance: "+appearance);
		this.description = description;
	}

	public virtual void Start(GameObject target, GameObject component, Transform transform) { 
		// Target is the main object, 
		// Component is the child gameObject that shows this upgrade
		// Transform is the transform of the components target. Manipulate for rotation scale and movement
		this.target = target;
		this.component = component;
		this.transform = transform;
	}

	public virtual void Update(){} // Call when the game updates

}
