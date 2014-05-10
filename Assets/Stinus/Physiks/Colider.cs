using UnityEngine;
using System.Collections;

public class Colider : MonoBehaviour {

	public static ArrayList Colidere = new ArrayList();

	private Vector2 hjorne;
	private float width;
	private float height;
	private IColiderResponse ICR;

	public void setColider(Vector2 _hjorne , int _width, int _height, IColiderResponse _ICR)
	{
		hjorne = _hjorne;
		width = _width;
		height = _height;
		ICR = _ICR;
		Colidere.Add(this);
	}

	public bool getIfColidingPoint(Vector3 _point)
	{
		Debug.Log("0 < " + (_point.x - transform.position.x ) + " < " +  width);
		Debug.Log("0 < " + (_point.y - transform.position.y ) + " < " +  height);
		if(transform.position.z == _point.z)
			if(_point.x - transform.position.x < width && _point.x - transform.position.x > 0)
				if(_point.y - transform.position.y  < height && _point.y - transform.position.y  > 0)
				{
					ICR.gotHit(new Vector2(_point.x, _point.y));
					return true;
				}


		return false;
	}

	void OnDrawGizmos() {
		Gizmos.color = Color.red;
		Vector3 v1 = new Vector3(transform.position.x + hjorne.x			,transform.position.y + height,0);
		Vector3 v2 = new Vector3(transform.position.x + hjorne.x + width	,transform.position.y + height,0);
		Vector3 v3 = new Vector3(transform.position.x + hjorne.x			,transform.position.y,0);
		Vector3 v4 = new Vector3(transform.position.x + hjorne.x + width	,transform.position.y,0);

		Gizmos.DrawLine(v1,v2);
		Gizmos.DrawLine(v1,v3);
		Gizmos.DrawLine(v3,v4);
		Gizmos.DrawLine(v2,v4);
	}
	
	// Use this for initialization
	void Start () 
	{

	}
	
	// Update is called once per frame
	void Update () 
	{

	}
}
