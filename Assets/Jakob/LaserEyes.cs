using UnityEngine;
using System.Collections;

/*
 * Remember: The image resource must be in the 'resources' folder 
 */

public class LaserEyes : Upgrade {

	private bool mouseDown = false;
	private GameObject laser;
	private static int shootButton = 0;

	public LaserEyes() {
		Init("Laser Eyes", UpgradeSlot.Eyes, "Eyeball", "LAZER EVERYTHING!");
	}

	public override void Start(GameObject target, GameObject component, Transform transform) { 
		base.Start(target, component, transform);
		Debug.Log("LAZER START!");
		Vector3 pos = component.transform.position;
		Debug.Log ("Laser pos: "+pos);
		laser = QuickSprite.CreateSprite("Laser", Vector2.zero, pos);
		laser.renderer.enabled = false;
	}

	private void ShootLazer() {

	}

	// Update is called once per frame
	public override void Update () {
		Vector3 look = Camera.main.ScreenToWorldPoint(Input.mousePosition);
		look.z = transform.position.z;
		transform.right = look - transform.position;

		if (Input.GetMouseButton(shootButton) && !mouseDown) {
			Debug.Log ("Mouse!");
			mouseDown = true;
			laser.renderer.enabled = true;
		} 
		if (Input.GetMouseButtonUp(shootButton) && mouseDown) {
			mouseDown = false;
			laser.renderer.enabled = false;
		}
		if (mouseDown) {
			//ShootLazer();
		}
	}
}
