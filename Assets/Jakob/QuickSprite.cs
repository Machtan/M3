using UnityEngine;
using System.Collections;

public static class QuickSprite {
	public static GameObject CreateSprite(string texture, Vector2 pivot, Vector3 position) {
		Texture2D tex = Resources.Load<Texture2D>(texture);
		Rect rect = new Rect(0, 0, tex.width, tex.height);
		return CreateSprite(Sprite.Create(tex, rect, pivot), position);
	}
	public static GameObject CreateSprite(Sprite sprite, Vector3 position) { 
		// Creates a centered sprite at the given position
		GameObject gam = new GameObject();
		SpriteRenderer ren = gam.AddComponent<SpriteRenderer>();
		ren.sprite = sprite;
		gam.transform.position = position;
		Debug.Log ("The new position is "+gam.transform.position+" ("+position+")");
		Rect r = sprite.rect;
		gam.transform.Translate(new Vector3(-r.width/2,-r.height/2, -2));
		gam.transform.localScale = new Vector3(r.width*3, r.height*3, 1);

		return gam;
	}
}
