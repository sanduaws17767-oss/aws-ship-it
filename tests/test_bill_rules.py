from pytest import approx

from bill_rules import (
    assess,
    data_transfer_cost,
    ec2_cost,
    nat_gateway_cost,
    rds_cost,
    s3_cost,
)


def test_zero_hours_costs_nothing():
    assert ec2_cost(0.0118, 0) == 0

def test_nat_gateway_cost():
    assert nat_gateway_cost(0.05,730,0.05,10) == 37

   
def test_full_month():
    assert ec2_cost(0.0118, 730) == approx(8.614)

def test_nat_costs_money_even_when_unused():
    assert nat_gateway_cost(0.05, 730, 0.05, 0) == approx(36.5)   


def test_s3_cost():
    assert s3_cost(0.024, 50) == approx(1.2)   

def test_rds_cost():
    assert rds_cost(0.019, 730, 0.133, 20) == approx(16.53) 

def test_transfer_under_free_allowance():
    assert data_transfer_cost(0.09, 50, 100) == 0

def test_transfer_over_free_allowance():
    assert data_transfer_cost(0.09, 150, 100) == approx(4.5)


def test_assess_totals_everything():
    result = assess("t3.micro", 730, "none",0, "no", 10, 50)
    assert result["total"] == approx(8.854)

def test_assess_handles_bad_input():
    result = assess("t3.micro", "abc", "none", 0, "no", 10, 50)
    assert "error" in result

def test_assess_rejects_negative_numbers():
    result = assess("t3.micro", -5, "none", 0, "no", 10, 50)
    assert "error" in result    

