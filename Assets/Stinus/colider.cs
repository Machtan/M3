using UnityEngine;
using System.Collections;

public class Colider : MonoBehaviour {

	public static ArrayList Colidere = new ArrayList();

	private Vector2 hjorne;
	private float width;
	private float height;

	public void setColider(Vector2 _hjorne , int _width, int _height)
	{
		hjorne = _hjorne;
		width = _width;
		height = _height;
		Colidere.Add(this);
	}

	public bool getIfColidingPoint(Vector3 _point)
	{
		if(transform.position.z == _point.z)
			if(_point.x - hjorne.x < width)
				if(_point.y - hjorne.y < height)
					return true;
		return false;
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
