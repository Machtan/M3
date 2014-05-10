using UnityEngine;
using System.Collections;

public class MoveScript : MonoBehaviour {

	public float moveSpeed = 80; // Units per second
	public Vector2 velocity = new Vector2(0,0);
	private Animator animator;
	//private Renderer renderer;
	private bool leftDown = false;
	private bool rightDown = false;

	// Use this for initialization
	void Start () {
		animator = this.GetComponent<Animator>();
		Debug.Log (animator);
	}

	void setWalkAnimation(bool on) {
		if (on) {
			animator.SetBool("Walking", true);
		} else {
			animator.SetBool ("Walking", false);
		}
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
		if (velocity != Vector2.zero) {
			if (!animator.GetBool("Walking")) {
				setWalkAnimation (true);
			}
			transform.Translate(velocity*Time.deltaTime);
		} else if (animator.GetBool ("Walking")) {
			setWalkAnimation (false);
		}
	}
}
