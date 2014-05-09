using UnityEngine;
using System.Collections;

public class MoveScript : MonoBehaviour {

	public float moveSpeed = 10; // Units per second
	public Vector2 velocity = new Vector2(0,0);
	private bool leftDown = false;
	private bool rightDown = false;

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown(KeyCode.RightArrow) && !rightDown) {
			rightDown = true;
			velocity.x += moveSpeed;
		} 
		if (Input.GetKeyUp (KeyCode.LeftArrow) && leftDown) {
			leftDown = false;
			velocity.x += moveSpeed;
		}
		if (Input.GetKeyDown (KeyCode.LeftArrow) && !leftDown) {
			leftDown = true;
			velocity.x -= moveSpeed;
		}
		if (Input.GetKeyUp (KeyCode.RightArrow) && rightDown) {
			rightDown = false;
			velocity.x -= moveSpeed;
		}

		transform.Translate(velocity*Time.deltaTime);
	}
}
